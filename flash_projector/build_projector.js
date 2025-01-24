// build_projector.js

// 1) Import the library class for Windows
const { ProjectorSaWindows } = require('@shockpkg/swf-projector');
const path = require('path');

async function build() {
  // 2) Create an instance of ProjectorSaWindows
  //    The constructor argument is the output EXE you want to create
  const projector = new ProjectorSaWindows('Flash.exe');

  // 3) Tell it where to find the base player (the official standalone projector)
  projector.player = path.resolve('player.exe');

  // 4) Point to your SWF
  projector.movieFile = path.resolve('default.swf');

  // 5) Optional icon, version strings, etc.
  //    Example: projector.iconFile = path.resolve('icon.ico');
  //    projector.versionStrings = {...};

  // 6) Patches to remove out-of-date warnings, code signature, etc. if desired
  // projector.removeCodeSignature = true;
  // projector.patchOutOfDateDisable = true;
  // projector.patchWindowTitle = 'My Custom Game';

  // 7) Actually build the EXE
  await projector.write();

  console.log('Projector EXE created: MyGameProjector.exe');
}

build().catch(err => {
  console.error('Error creating projector:', err);
});
