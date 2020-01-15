import React, { useLayoutEffect, useState } from 'react';
import mapboxgl from 'mapbox-gl';
import { fallbackRasterStyle } from '../projects/projectsMap';
import { MAPBOX_TOKEN } from '../../config';

const UserCountriesMap = () => {
  const [map, setMap] = useState(null);

  const mapRef = React.createRef();

  useLayoutEffect(() => {
    if (map === null) {
      setMap(
        new mapboxgl.Map({
          container: mapRef.current,
          style: MAPBOX_TOKEN ? 'mapbox://styles/mapbox/light-v10' : fallbackRasterStyle,
          zoom: 0,
        }),
      );
    }
    return () => {
      map && map.remove();
    };
  }, [map, mapRef]);

  return <div id="map" className="w-50 fl" ref={mapRef}></div>;
};

const CountriesTable = ({ countries }) => {
  const nth = n => {
    return ['st', 'nd', 'rd'][((((n + 90) % 100) - 10) % 10) - 1] || 'th';
  };

  return (
    <table class="f6 w-100 mw8 center" cellspacing="0">
      <thead className="blue-grey b">
        <tr>
          <th className="w-10 pv3 bt bb b--light-gray"></th>
          <th className="w-30 pv3 bt bb b--light-gray">Country</th>
          <th className="w-20 pv3 bt bb b--light-gray">Tasks mapped</th>
          <th className="w-20 pv3 bt bb b--light-gray">Tasks validated</th>
          <th className="w-20 pv3 bt bb b--light-gray">Total</th>
        </tr>
      </thead>
      <tbody>
        {countries.map((c, i) => {
          let pos = i + 1;
          return (
            <tr>
              <td className="flex items-start blue-grey b pv3 bb b--light-gray">
                {pos}
                {nth(pos)}
              </td>
              <td className="bb b--light-gray ">{c.name}</td>
              <td className="bb b--light-gray tc">{c.mapped}</td>
              <td className="bb b--light-gray tc">{c.validated}</td>
              <td className="bb b--light-gray tc">{c.total}</td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
};

export const CountriesMapped = () => {
  const countries = [
    { name: 'India', mapped: 30, validated: 24, total: 54 },
    { name: 'Kuwait', mapped: 12, validated: 0, total: 12 },
    { name: 'Democratic Republic of Congo', mapped: 30, validated: 0, total: 30 },
    { name: 'Papua New Guinea', mapped: 42, validated: 0, total: 42 },
    { name: 'Central African Republic', mapped: 42, validated: 0, total: 42 },
  ];

  return (
    <div className="bg-white pa3">
      <h3 className="f3 blue-dark mt0 fw6 pt3">Countries most mapped</h3>
      <div className="w-100 cf flex items-stretch">
        <div className="w-50 fl">
          <CountriesTable countries={countries} />
        </div>
        <UserCountriesMap />
      </div>
    </div>
  );
};
