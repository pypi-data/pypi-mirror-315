#!/usr/bin/env python
# Copyright Salient Predictions 2024

"""Hydrology functions."""

import numpy as np
import pandas as pd
import requests
import xarray as xr

from .geo_api import geo
from .location import Location

# Dictionary mapping salientsdk.geo_api.VARIABLES to VIC parameters
_GEO_VIC_PARAMS = {"elevation": {"name": "elev", "dtype": "float64"}}


def calc_swe(met: xr.Dataset, timedim: str = "forecast_day") -> xr.DataArray:
    """Call the `snow17` model for each location and ensemble member.

    Acknowledgements: Based on Anderson (2006) and Mark Raleigh's matlab code.

    Primary Citations:
    1.  Anderson, E. A. (1973), National Weather Service River Forecast System
    Snow   Accumulation   and   Ablation   Model,   NOAA   Tech.   Memo.   NWS
    HYDro-17, 217 pp., U.S. Dep. of Commer., Silver Spring, Md.
    2.  Anderson, E. A. (1976), A point energy and mass balance model of a snow
    cover, NOAA Tech. Rep. 19, 150 pp., U.S. Dep. of Commer., Silver Spring, Md.

    Written by Joe Hamman April, 2013

    Args:
        met (xr.Dataset): a dataset containing `timedim`, `precip`, `temp`, & `lat`.
            If `met` contains a field `elevation` it will be used.
        timedim (str): the name of the time dimension in `met`
            The time step in `timedim` can be `hourly` or `daily`.

    Returns:
        xr.DataArray: a dataset containing snow water equivalent (mm)
    """
    elev = met["elevation"] if "elevation" in met else 0
    dt = _get_timestep_hours(met[timedim])  # 1 = hourly, 24 = daily frequency
    # snow17 needs a vector of datetime objects to call timetuple()
    time = pd.DatetimeIndex(met[timedim].values).to_pydatetime()

    # Apply the snow model over all locations and all ensembles
    (swe, outflow) = xr.apply_ufunc(
        snow17,
        time,  # time,
        met.precip,  # prec,
        met.temp,  # tair,
        met.lat,  # lat
        elev,  # elevation
        dt,  # dt
        input_core_dims=[[timedim], [timedim], [timedim], [], [], []],
        output_core_dims=[[timedim], [timedim]],
        vectorize=True,
    )

    # After calling ufunc, swe will have timedim last.  Force it to match others:
    swe = swe.transpose(*met.temp.dims)

    swe.attrs = {"short_name": "swe", "long_name": "Snow Water Equivalent", "units": "mm"}

    return swe


def _get_timestep_hours(time_array: xr.DataArray) -> float:
    """Return the timestep of a datetime array in hours."""
    t0, t1 = time_array[:2]
    return ((t1 - t0) / np.timedelta64(1, "h")).item()


def snow17(
    time,
    prec,
    tair,
    lat=50,
    elevation=0,
    dt=24,
    scf=1.0,
    rvs=1,
    uadj=0.04,
    mbase=1.0,
    mfmax=1.05,
    mfmin=0.6,
    tipm=0.1,
    nmf=0.15,
    plwhc=0.04,
    pxtemp=1.0,
    pxtemp1=-1.0,
    pxtemp2=3.0,
):
    """Snow-17 accumulation and ablation model.

    This version of Snow-17 is intended for use at a point location.
    The time steps for precipitation and temperature must be equal for this
    code.

    Args:
        time (1d numpy.ndarray or scalar): Array of datetime objects.
        prec (1d numpy.ndarray or scalar): Array of precipitation forcings, size of `time`.
        tair (1d numpy.ndarray or scalar): Array of air temperature forcings, size of `time`.
        lat (float, optional): Latitude of simulation point or grid cell. Defaults to None.
        elevation (float, optional): Elevation of simulation point or grid cell. Defaults to 0.
        dt (float, optional): Timestep in hours. Defaults to 24 hours but should always match the timestep in `time`.
        scf (float, optional): Gauge under-catch snow correction factor. Defaults to 1.0.
        rvs ({0, 1, 2}, optional): Rain vs. Snow option. Default value of 1 is a linear transition between 2 temperatures (pxtemp1 and pxtemp2).
        uadj (float, optional): Average wind function during rain on snow (mm/mb). Defaults to 0.04, based on data from the American River Basin (Shamir & Georgakakos 2007).
        mbase (float, optional): Base temperature above which melt typically occurs (deg C). Defaults to 1.0, based on data from the American River Basin (Shamir & Georgakakos 2007). Must be greater than 0 deg C.
        mfmax (float, optional): Maximum melt factor during non-rain periods (mm/deg C 6 hr) - in western facing slope assumed to occur on June 21. Defaults to 1.05, based on data from the American River Basin (Shamir & Georgakakos 2007).
        mfmin (float, optional): Minimum melt factor during non-rain periods (mm/deg C 6 hr) - in western facing slope assumed to occur on December 21. Defaults to 0.60, based on data from the American River Basin (Shamir & Georgakakos 2007).
        tipm (float, optional): Model parameter (>0.0 and <1.0) - Anderson Manual recommends 0.1 to 0.2 for deep snowpack areas. Defaults to 0.1.
        nmf (float, optional): Percent liquid water holding capacity of the snow pack - max is 0.4. Defaults to 0.04, based on data from the American River Basin (Shamir & Georgakakos 2007).
        plwhc (float, optional): Percent liquid water holding capacity of the snow pack - max is 0.4. Defaults to 0.04, based on data from the American River Basin (Shamir & Georgakakos 2007).
        pxtemp (float, optional): Temperature dividing rain from snow, deg C - if temp is less than or equal to pxtemp, all precip is snow. Otherwise, it is rain. Defaults to 1.0.
        pxtemp1 (float, optional): Lower Limit Temperature dividing transition from snow, deg C - if temp is less than or equal to pxtemp1, all precip is snow. Otherwise, it is mixed linearly. Defaults to -1.0.
        pxtemp2 (float, optional): Upper Limit Temperature dividing rain from transition, deg C - if temp is greater than or equal to pxtemp2, all precip is rain. Otherwise, it is mixed linearly. Defaults to 3.0.

    Returns:
        model_swe (numpy.ndarray): Simulated snow water equivalent.
        outflow (numpy.ndarray): Simulated runoff outflow.
    """
    # Convert to numpy array if scalars
    time = np.asarray(time)
    prec = np.asarray(prec)
    tair = np.asarray(tair)

    assert time.shape == prec.shape == tair.shape

    # Initialization
    # Antecedent Temperature Index, deg C
    ait = 0.0
    # Liquid water capacity
    w_qx = 0.0
    # Liquid water held by the snow (mm)
    w_q = 0.0
    # accumulated water equivalent of the iceportion of the snow cover (mm)
    w_i = 0.0
    # Heat deficit, also known as NEGHS, Negative Heat Storage
    deficit = 0.0

    # number of time steps
    nsteps = len(time)
    model_swe = np.zeros(nsteps)
    outflow = np.zeros(nsteps)

    # Stefan-Boltzman constant (mm/K/hr)
    stefan = 6.12 * (10 ** (-10))
    # atmospheric pressure (mb) where elevation is in HUNDREDS of meters
    # (this is incorrectly stated in the manual)
    p_atm = 33.86 * (29.9 - (0.335 * elevation / 100) + (0.00022 * ((elevation / 100) ** 2.4)))

    transitionx = [pxtemp1, pxtemp2]
    transitiony = [1.0, 0.0]

    tipm_dt = 1.0 - ((1.0 - tipm) ** (dt / 6))

    # Model Execution
    for i, t in enumerate(time):
        mf = melt_function(t, dt, lat, mfmax, mfmin)

        # air temperature at this time step (deg C)
        t_air_mean = tair[i]
        # precipitation at this time step (mm)
        precip = prec[i]

        # Divide rain and snow
        if rvs == 0:
            if t_air_mean <= pxtemp:
                # then the air temperature is cold enough for snow to occur
                fracsnow = 1.0
            else:
                # then the air temperature is warm enough for rain
                fracsnow = 0.0
        elif rvs == 1:
            if t_air_mean <= pxtemp1:
                fracsnow = 1.0
            elif t_air_mean >= pxtemp2:
                fracsnow = 0.0
            else:
                fracsnow = np.interp(t_air_mean, transitionx, transitiony)
        elif rvs == 2:
            fracsnow = 1.0
        else:
            raise ValueError("Invalid rain vs snow option")

        fracrain = 1.0 - fracsnow

        # Snow Accumulation
        # water equivalent of new snowfall (mm)
        pn = precip * fracsnow * scf
        # w_i = accumulated water equivalent of the ice portion of the snow
        # cover (mm)
        w_i += pn
        e = 0.0
        # amount of precip (mm) that is rain during this time step
        rain = fracrain * precip

        # Temperature and Heat deficit from new Snow
        if t_air_mean < 0.0:
            t_snow_new = t_air_mean
            # delta_hd_snow = change in the heat deficit due to snowfall (mm)
            delta_hd_snow = -(t_snow_new * pn) / (80 / 0.5)
            t_rain = pxtemp
        else:
            t_snow_new = 0.0
            delta_hd_snow = 0.0
            t_rain = t_air_mean

        # Antecedent temperature Index
        if pn > (1.5 * dt):
            ait = t_snow_new
        else:
            # Antecedent temperature index
            ait = ait + tipm_dt * (t_air_mean - ait)
        if ait > 0:
            ait = 0

        # Heat Exchange when no Surface melt
        # delta_hd_t = change in heat deficit due to a temperature gradient(mm)
        delta_hd_t = nmf * (dt / 6.0) * ((mf) / mfmax) * (ait - t_snow_new)

        # Rain-on-snow melt
        # saturated vapor pressure at t_air_mean (mb)
        e_sat = 2.7489 * (10**8) * np.exp((-4278.63 / (t_air_mean + 242.792)))
        # 1.5 mm/ 6 hrs
        if rain > (0.25 * dt):
            # melt (mm) during rain-on-snow periods is:
            m_ros1 = np.maximum(stefan * dt * (((t_air_mean + 273) ** 4) - (273**4)), 0.0)
            m_ros2 = np.maximum((0.0125 * rain * t_rain), 0.0)
            m_ros3 = np.maximum(
                (
                    8.5
                    * uadj
                    * (dt / 6.0)
                    * (((0.9 * e_sat) - 6.11) + (0.00057 * p_atm * t_air_mean))
                ),
                0.0,
            )
            m_ros = m_ros1 + m_ros2 + m_ros3
        else:
            m_ros = 0.0

        # Non-Rain melt
        if rain <= (0.25 * dt) and (t_air_mean > mbase):
            # melt during non-rain periods is:
            m_nr = (mf * (t_air_mean - mbase)) + (0.0125 * rain * t_rain)
        else:
            m_nr = 0.0

        # Ripeness of the snow cover
        melt = m_ros + m_nr
        if melt <= 0:
            melt = 0.0

        if melt < w_i:
            w_i = w_i - melt
        else:
            melt = w_i + w_q
            w_i = 0.0

        # qw = liquid water available melted/rained at the snow surface (mm)
        qw = melt + rain
        # w_qx = liquid water capacity (mm)
        w_qx = plwhc * w_i
        # deficit = heat deficit (mm)
        deficit += delta_hd_snow + delta_hd_t

        # limits of heat deficit
        if deficit < 0:
            deficit = 0.0
        elif deficit > 0.33 * w_i:
            deficit = 0.33 * w_i

        # Snow cover is ripe when both (deficit=0) & (w_q = w_qx)
        if w_i > 0.0:
            if (qw + w_q) > ((deficit * (1 + plwhc)) + w_qx):
                # THEN the snow is RIPE
                # Excess liquid water (mm)
                e = qw + w_q - w_qx - (deficit * (1 + plwhc))
                # fills liquid water capacity
                w_q = w_qx
                # w_i increases because water refreezes as heat deficit is
                # decreased
                w_i = w_i + deficit
                deficit = 0.0
            elif (qw >= deficit) and ((qw + w_q) <= ((deficit * (1 + plwhc)) + w_qx)):
                # ait((qw + w_q) <= ((deficit * (1 + plwhc)) + w_qx))):  BUG???
                # https://github.com/UW-Hydro/tonic/issues/78
                # THEN the snow is NOT yet ripe, but ice is being melted
                e = 0.0
                w_q = w_q + qw - deficit
                # w_i increases because water refreezes as heat deficit is
                # decreased
                w_i = w_i + deficit
                deficit = 0.0
            else:
                # (qw < deficit) %elseif ((qw + w_q) < deficit):
                # THEN the snow is NOT yet ripe
                e = 0.0
                # w_i increases because water refreezes as heat deficit is
                # decreased
                w_i = w_i + qw
                deficit = deficit - qw
            swe = w_i + w_q
        else:
            e = qw
            swe = 0

        if deficit == 0:
            ait = 0

        # End of model execution
        model_swe[i] = swe  # total swe (mm) at this time step
        outflow[i] = e

    return model_swe, outflow


def melt_function(t, dt, lat, mfmax, mfmin):
    """Seasonal variation calcs - indexed for Non-Rain melt.

    Args:
        t (datetime): Datetime object for the current timestep.
        dt (float): Timestep duration in hours.
        lat (float): Latitude of the simulation point or grid cell.
        mfmax (float): Maximum melt factor during non-rain periods (mm/deg C per 6 hours),
            typically occurring on June 21. The default value of 1.05 is based on data from
            the American River Basin (Shamir & Georgakakos, 2007).
        mfmin (float): Minimum melt factor during non-rain periods (mm/deg C per 6 hours),
            typically occurring on December 21. The default value of 0.60 is based on data from
            the American River Basin (Shamir & Georgakakos, 2007).

    Returns:
        float: Melt function value for the current timestep.
    """
    tt = t.timetuple()
    jday = tt[-2]
    n_mar21 = jday - 80
    days = 365

    # seasonal variation
    sv = (0.5 * np.sin((n_mar21 * 2 * np.pi) / days)) + 0.5
    if lat < 54:
        # latitude parameter, av=1.0 when lat < 54 deg N
        av = 1.0
    else:
        if jday <= 77 or jday >= 267:
            # av = 0.0 from September 24 to March 18,
            av = 0.0
        elif jday >= 117 and jday <= 227:
            # av = 1.0 from April 27 to August 15
            av = 1.0
        elif jday >= 78 and jday <= 116:
            # av varies linearly between 0.0 and 1.0 from 3/19-4/26 and
            # between 1.0 and 0.0 from 8/16-9/23.
            av = np.interp(jday, [78, 116], [0, 1])
        elif jday >= 228 and jday <= 266:
            av = np.interp(jday, [228, 266], [1, 0])
    meltf = (dt / 6) * ((sv * av * (mfmax - mfmin)) + mfmin)

    return meltf


def _build_vic_params(
    # API arguments -----
    loc: Location,
    resolution: float = 0.25,
    # Non-API arguments --------
    destination: str = "-default",
    force: bool = False,
    session: requests.Session | None = None,
    apikey: str | None = None,
    verify: bool | None = None,
    verbose: bool = False,
    **kwargs,
) -> str | list[str]:
    """Build Variable Infiltration Capicity (VIC) model land surface parameter NetCDF file.

    Args:
        loc (Location): The location to query. This location must be a shapefile with one or more polygons defining the location.
        resolution (float): The spatial resolution of the data in degrees.
        destination (str): The destination directory for downloaded files.
        force (bool): If False (default), don't download the data if it already exists
        session (requests.Session): The session object to use for the request
        apikey (str | None): The API key to use for the request.
            In most cases, this is not needed if a `session` is provided.
        verify (bool): If True (default), verify the SSL certificate
        verbose (bool): If True (default False) print status messages
        **kwargs: Additional arguments to pass to the API

    Returns:
        str | pd.DataFrame : If only one file was downloaded, return the name of the file.
            If multiple files were downloaded, return a table with column `file_name` and
            additional columns documenting the vectorized input arguments such as
            `location_file`.
    """
    assert (
        loc.shapefile is not None
    ), "The input location must must be a shapefile with one or more polygons defining the location."

    files = geo(
        loc=loc,
        variables=["elevation"],
        resolution=resolution,
        format="nc",
        destination=destination,
        force=force,
        session=session,
        apikey=apikey,
        verify=verify,
        verbose=verbose,
        kwargs=kwargs,
    )

    if isinstance(files, pd.DataFrame):
        file_names = files["file_name"].apply(_transform_geo_to_vic_params)
        files["file_name"] = file_names
        return files
    else:
        return _transform_geo_to_vic_params(files)


def _transform_geo_to_vic_params(path: str) -> str:
    """Transform variables of a NetCDF file return from the geo endpoint to VIC parameters.

    Args:
        path (str): Path to NetCDF file return from the geo endpoint.

    Returns:
        str: Path to NetCDF file transformed to VIC parameters.
    """
    vic_path = path.replace("geo", "vic_params")
    ds = xr.open_dataset(path)
    for data_var in ds.data_vars:
        config = _GEO_VIC_PARAMS[data_var]
        ds[data_var] = ds[data_var].astype(config["dtype"])
        ds = ds.rename_vars({data_var: config["name"]})
    ds.to_netcdf(vic_path)
    return vic_path
