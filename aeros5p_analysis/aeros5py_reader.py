#!/bin/python
import numpy as np
import pandas as pd

def read_l1b(directory):
    nbands = int(1/4 * (sum(1 for line in open(directory)) -3))

    data = dict()

    filename = directory.split('/')[-1]
    for n in range(nbands):
        data[f'BAND{n+1}'] = dict()

    with open(directory, 'r') as l1b :
        for _ in range(3): l1b.readline()
        for bd in data.keys():
            data[bd]['lambdas_rad'] = np.array(l1b.readline().split(), dtype=float)
            data[bd]['rad'] = np.array(l1b.readline().split(), dtype=float)
            data[bd]['lambdas_irrad'] = np.array(l1b.readline().split(),dtype=float)
            data[bd]['irrad'] = np.array(l1b.readline().split(),dtype=float)

    directory_err = directory.replace('L1B','ERR')
    with open(directory_err, "r") as err :
        data['BAND1']['rad_err'] = np.array(err.readline().split(), dtype=float)
        data['BAND2']['rad_err'] = np.array(err.readline().split(), dtype=float)
        data['BAND3']['rad_err'] = np.array(err.readline().split(), dtype=float)
        data['BAND4']['rad_err'] = np.array(err.readline().split(), dtype=float)
        data['BAND1']['irrad_err'] = np.array(err.readline().split(), dtype=float)
        data['BAND2']['irrad_err'] = np.array(err.readline().split(), dtype=float)
        data['BAND3']['irrad_err'] = np.array(err.readline().split(), dtype=float)
        data['BAND4']['irrad_err'] = np.array(err.readline().split(), dtype=float)
    return data

def read_reflectance(directory) : 
    h='Lambda Reflectances_vlidort Reflectances_gome2soft err1 err2 err3 err4'
    reflectance_sim = pd.read_csv(directory, skipinitialspace=True, delim_whitespace=True, skiprows=5, names=h.split())
    return reflectance_sim

def read_aod_nc(output_path, input_path, date):
  import netCDF4 as nc
  import pandas as pd
  filters = {} #'rms':(0,15), 'dof':(0.75,3)}
  b = nc.Dataset(output_path + '/log_a_AOD_vlidort_all.nc', 'r')
  aod0 = b['aod'][:]
  aod_layer = b['aod_layer'][:]
  h0 = b['surface_level'][:]
  totcol = b['totcol'][:]
  wavelength = b['wavelength'][:]
  rms = b['rms'][:]
  dof = b['dof'][:]
  viirs = b['viirs_cloud_mask'][:]
  cf = b['s5p_cloud_fraction'][:]
  coo = pd.DataFrame({'pix':b['pixel_id'][:], 'lon':b['lon'][:], 'lat':b['lat'][:]})
  longitude = b['lon'][:]
  latitude = b['lat'][:]
  pixnum1 = b['pixel_id'][:]
  reflectance_sim = b['reflectance_sim'][:]
  reflectance_meas = b['reflectance_meas'][:]
  v_wavelength = b['v_wavelength'][:]

  v_wavelength[v_wavelength == -9999] = np.nan
  reflectance_sim[v_wavelength == -9999] = np.nan
  reflectance_meas[v_wavelength == -9999] = np.nan
  
  AOD440, AOD675 = aod0[:,57], aod0[:,160]
  alpha = - np.log(AOD440/AOD675)/np.log(wavelength[57]/wavelength[160])
  aod550 = aod0[:,150]


  aod = {"aerosol_optical_depth":aod0,
         "aod_layer":np.fliplr(aod_layer),
         "lambdas":wavelength,
         "rms":rms,
         "dof":dof,
         "viirs_cloud_mask":viirs,
         "cloud_fraction":cf,
         "surface_height":h0,
         "totcol":totcol * 1e-5,
         "alpha": alpha,
         "aerosol_optical_depth[550nm]": aod550,
         "lon_centre":longitude,
         "lat_centre":latitude,
         "pixnum1":pixnum1,
         "reflectance_sim":reflectance_sim,
         "reflectance_meas":reflectance_meas,
         "v_wavelength":v_wavelength,
        }

  for fil in filters :
    aod['lat_centre'][aod[fil]>filters[fil][1]] = np.nan
    aod['aerosol_optical_depth'][aod[fil]>filters[fil][1]] = np.nan
    aod['lon_centre'][aod[fil]<filters[fil][0]] = np.nan
    aod['aerosol_optical_depth'][aod[fil]<filters[fil][0]] = np.nan
    aod['dof'][aod[fil]<filters[fil][0]] = np.nan
    aod['rms'][aod[fil]<filters[fil][0]] = np.nan
    aod['dof'][aod[fil]>filters[fil][1]] = np.nan
    aod['rms'][aod[fil]>filters[fil][1]] = np.nan
    aod['surface_height'][aod[fil]<filters[fil][0]] = np.nan
    aod['surface_height'][aod[fil]>filters[fil][1]] = np.nan

  return aod
