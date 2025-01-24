# Portable Executable Signature

Package for reading and writing PE code signatures (but not creating them)

[![npm](https://img.shields.io/npm/v/portable-executable-signature.svg)](https://npmjs.com/package/portable-executable-signature)
[![node](https://img.shields.io/node/v/portable-executable-signature.svg)](https://nodejs.org)

[![size](https://packagephobia.now.sh/badge?p=portable-executable-signature)](https://packagephobia.now.sh/result?p=portable-executable-signature)
[![downloads](https://img.shields.io/npm/dm/portable-executable-signature.svg)](https://npmcharts.com/compare/portable-executable-signature?minimal=true)

[![main](https://github.com/AlexanderOMara/portable-executable-signature/actions/workflows/main.yaml/badge.svg)](https://github.com/AlexanderOMara/portable-executable-signature/actions/workflows/main.yaml)

# Overview

A broken code signature is often worse than no signature, so it can be desirable to remove a signature.

This package can remove code signatures from PE binaries.

# Usage

Just pass an `ArrayBuffer` or an object that is a view of an `ArrayBuffer` to the `signatureGet` and `signatureSet` functions.

```js
import {readFile, writeFile} from 'node:fs/promises';
import {signatureGet, signatureSet} from 'portable-executable-signature';

const data = await readFile('pe-binary.exe');
const signature = signatureGet(data);
console.log('signature:', signature);
const unsigned = signatureSet(data, null);
console.log('unsigned:', unsigned);
await writeFile('pe-binary-unsigned.exe', Buffer.from(unsigned));
```

# Bugs

If you find a bug or have compatibility issues, please open a ticket under issues section for this repository.

# License

Copyright (c) 2019-2024 Alexander O'Mara

Licensed under the Mozilla Public License, v. 2.0.

If this license does not work for you, feel free to contact me.
