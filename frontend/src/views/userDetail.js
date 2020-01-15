import React from 'react';
import { HeaderProfile } from '../components/userDetail/headerProfile';
import { ElementsMapped } from '../components/userDetail/elementsMapped';
import { CountriesMapped } from '../components/userDetail/countriesMapped';
import { TopProjects } from '../components/userDetail/topProjects';

export const UserDetail = ({ username }) => {
	const blockWidth = 'w-80 center';
	const blockStyle = { width: '31%' };

	return (
		<div className="bg-light-gray w-100">
			<div className="bg-white w-100">
				<div className="w-80 cf center pt4 pb3">
					<HeaderProfile />
				</div>
			</div>
			<div className={blockWidth}>
				<div className="mv4">
					<ElementsMapped />
				</div>
				<div className="mv4 cf">
					<div className="w-100 flex justify-between content-stretch">
						<div style={blockStyle} className="bg-white pa3">
							<h3 className="f3 blue-dark mt0 fw6 pt3">Edits by number</h3>
							<p>hola</p>
							<p>hola</p>
							<p>hola</p>
						</div>
						<div style={blockStyle} className="bg-white pa3">
							<TopProjects />
						</div>
						<div style={blockStyle} className="bg-white pa3">
							<h3 className="f3 blue-dark mt0 fw6 pt3">Edits by number</h3>
						</div>
					</div>
				</div>
				<div className="mv4 cf">
					<CountriesMapped />
				</div>
			</div>
		</div>
	);
};
