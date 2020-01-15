import React from 'react';
import { TwitterIcon, FacebookIcon, EnvelopeIcon, LinkedinIcon } from '../svgIcons';

const SocialMedia = () => {
  const socialMediaItems = ['emailAddress', 'twitterId', 'facebookId', 'linkedinId'];

  const data = {
    emailAddress: 'jorge@hotosm.org',
    twitterId: '_jorgemartinezg',
    facebookId: 'facebook.com/jorgemartinez',
    linkedinId: 'linkedin.com/jorgemartinez',
  };

  const getSocialIcon = field => {
    const iconStyle = {
      width: '1em',
      height: '1em',
      padding: '0.5em',
      backgroundColor: 'black',
      color: 'white',
    };
    const iconClass = 'mr2 br-100';

    switch (field) {
      case 'emailAddress':
        return <EnvelopeIcon style={iconStyle} className={iconClass} />;
      case 'twitterId':
        return <TwitterIcon style={iconStyle} className={iconClass} />;
      case 'facebookId':
        return <FacebookIcon style={iconStyle} className={iconClass} />;
      case 'linkedinId':
        return <LinkedinIcon style={iconStyle} className={iconClass} />;
      default:
        return null;
    }
  };

  return (
    <ul className="list pa0">
      {socialMediaItems.map(i => {
        return (
          <li className="dib mr3 cf f7">
            <div className="mr2 flex items-center">
              <div className="mr2 h2 flex items-center">
                {getSocialIcon(i)} {data[i]}
              </div>
            </div>
          </li>
        );
      })}
    </ul>
  );
};

export const HeaderProfile = () => {
  return (
    <div>
      <div className="bg-white w-10 fl mr4">
        <div className="bg-light-gray h4 w4 br-100"></div>
      </div>
      <div className="bg-white w-80 fl">
        <div className="mb4">
          <p className="barlow-condensed f2 ttu b ma0 mb2">Jorge Martinez</p>
          <p className="f5 ma0 mb2">Beginner mapper</p>
          <p className="f6 ma0 blue-grey">457/600 tasks to intermediate</p>
        </div>
        <SocialMedia />
      </div>
    </div>
  );
};
