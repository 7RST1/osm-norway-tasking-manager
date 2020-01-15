import React from 'react';
import { ClockIcon } from '../svgIcons';

const Element = ({ last }) => {
	return (
		<div style={{ width: '19%' }} className="pv3 ph2 flex bg-white items-center ">
			<div className="w-40 tc">
				<ClockIcon className="h-50 w-50" />
			</div>
			<div className="w-60">
				<p className="ma0 mb2 barlow-condensed b f3"> 12h 48m </p>
				<p className="ma0 mb2 f7 b blue-grey"> Time spent mapping </p>
			</div>
		</div>
	);
};

export const ElementsMapped = () => {
	return (
		<div className="flex justify-between">
			<Element />
			<Element />
			<Element />
			<Element />
			<Element last={true} />
		</div>
	);
};
