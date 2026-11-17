import React from 'react';
import {Composition} from 'remotion';
import {Graphic} from './Graphic';
import {COMPS} from './gfx_data';

export const Root: React.FC = () => (
  <>
    {COMPS.map((c) => (
      <Composition
        key={c.id}
        id={c.id}
        component={Graphic}
        durationInFrames={c.frames}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{section: c.section, description: c.description}}
      />
    ))}
  </>
);
