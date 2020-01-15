import React from 'react';
import { FormattedMessage, FormattedNumber } from 'react-intl';

import messages from './messages';
import { PROFILE_RELEVANT_FIELDS } from './forms';

export function CompletenessProgressBar(props: Object) {
  return (
    <>
      <div className="cf db">
        <div className="w-90 pr2 pt2 fl relative">
          <div
            className={'absolute br-pill hhalf hide-child ' + props.color}
            style={{ width: `${props.completeness.toPrecision(3) * 100}%` }}
          ></div>
          <div className={'bg-grey-light br-pill hhalf hide-child overflow-y-hidden'}></div>
        </div>
        {props.children}
      </div>
    </>
  );
}

export function calculateCompleteness(userDetails) {
  return (
    PROFILE_RELEVANT_FIELDS.filter(k => userDetails[k]).length / PROFILE_RELEVANT_FIELDS.length
  );
}

export function ProfileCompleteness({ userDetails }: Object) {
  const completeness = calculateCompleteness(userDetails);
  return (
    <div className="shadow-4 bg-white ph3 pv3">
      <h3 className="blue-dark f4 mt0 fw6">
        <FormattedMessage {...messages.completenessTitle} />
      </h3>
      <p className="blue-grey">
        {completeness === 0 && <FormattedMessage {...messages.completenessLead0} />}
        {completeness > 0 && completeness < 1 && (
          <FormattedMessage {...messages.completenessLead1} />
        )}
        {completeness === 1 && <FormattedMessage {...messages.completenessLead2} />}
      </p>
      <CompletenessProgressBar completeness={completeness} color="bg-red">
        <div className="w-10 fl pl1 fw6">
          <FormattedNumber
            value={completeness}
            maximumFractionDigits={0}
            style="percent" // eslint-disable-line react/style-prop-object
          />
        </div>
      </CompletenessProgressBar>
    </div>
  );
}
