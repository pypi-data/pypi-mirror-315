#!/bin/bash

# Commands to be run to recreate the testdata resources.
#
# NOTE: requires /mnt/CEPH_PROJECTS/FACT_CLIMAX to be mounted and accessible.

indices=('amt' 'spi12')
scenarios=('rcp45' 'rcp85')

idir_root="/mnt/CEPH_PROJECTS/FACT_CLIMAX/CORDEX-Adjust/INDICES/"
odir_root="./testdata/INDICES/"

# directories
for index in ${indices[@]}; do
    for scenario in ${scenarios[@]}
    do
        mkdir -p "${odir_root}/${index}/${scenario}"
    done
done

# copy/rescale indices (5-model ensembles)
for index in ${indices[@]}; do
    for scenario in ${scenarios[@]}; do
        idir="${idir_root}/${index}/${scenario}/"
        odir="${odir_root}/${index}/${scenario}/"
        for ncfile in $( find ${idir} -name "${index}*.nc" | head -n 5 )
        do
            echo "Rescaling ${ncfile}..."
            ofile="${odir}/$(basename "$ncfile")"
            gdal_translate -of NETCDF -outsize 2 2 "$ncfile" "$ofile" >/dev/null
            # gdal_translate converts dimensionless "1" units to float type, causing xarray to fail loading
            units=$( ncdump -h "$ofile" | sed -n "s/^.*${index}:units = \(.*\) ;/\1/p" )
            [[ "$units" = "1" ]] && ncatted -h -O -a units,${index},o,c,"1" "$ofile"
        done
    done
done

# dem
demfile="${idir_root}/DEM_1km_LAEA.nc"
echo "Rescaling ${demfile}..."
gdal_translate -of NETCDF -outsize 10 10 "$demfile" "${odir_root}/$(basename "$demfile")" >/dev/null
