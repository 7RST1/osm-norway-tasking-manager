import React from 'react';
import { CompletenessProgressBar } from '../user/completeness';

export const TopProjects = () => {
  const data = [
    { id: 6502, name: 'Cyclone Gaja', tasksNo: 30 },
    { id: 5691, name: 'Tanzania missing buildings', tasksNo: 15 },
    { id: 5170, name: 'Indian flood response', tasksNo: 10 },
    { id: 5260, name: '2018 Ebola', tasksNo: 2 },
  ];

  const tasksNo = data.map(d => d.tasksNo);
  const maxTaskNo = Math.max(...tasksNo);

  const tasksPercent = data.map(d => {
    return { ...d, percent: d.tasksNo / maxTaskNo };
  });

  return (
    <div>
      <h3 className="f3 blue-dark mt0 fw6 pt3">Top Projects contributed</h3>
      <ol className="pa0">
        {tasksPercent.map((p, i) => (
          <li className="w-100 flex blue-grey pv3">
            <div className="w-10 b f6">{i + 1}.</div>
            <div className="w-90">
              <p className="ma0 f6">
                #{p.id} - {p.name}
              </p>
              <CompletenessProgressBar
                completeness={Math.min(p.percent, 0.96)}
                color="bg-blue-dark"
              />
            </div>
            <div className="w-20 tl self-end">
              <p className="ma0 f6">{p.tasksNo} tasks</p>
            </div>
          </li>
        ))}
      </ol>
    </div>
  );
};
