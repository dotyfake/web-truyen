{
  "name": "yauzl",
  "version": "2.10.0",
  "description": "yet another unzip library for node",
  "main": "index.js",
  "scripts": {
    "test": "node test/test.js",
    "test-cov": "istanbul cover test/test.js",
    "test-travis": "istanbul cover --report lcovonly test/test.js"
  },
  "repository": {
    "type": "git",
    "url": "https://github.com/thejoshwolfe/yauzl.git"
  },
  "keywords": [
    "unzip",
    "zip",
    "stream",
    "archive",
    "file"
  ],
  "author": "Josh Wolfe <thejoshwolfe@gmail.com>",
  "license": "MIT",
  "bugs": {
    "url": "https://github.com/thejoshwolfe/yauzl/issues"
  },
  "homepage": "https://github.com/thejoshwolfe/yauzl",
  "dependencies": {
    "fd-slicer": "~1.1.0",
    "buffer-crc32": "~0.2.3"
  },
  "devDependencies": {
    "bl": "~1.0.0",
    "istanbul": "~0.3.4",
    "pend": "~1.2.0"
  },
  "files": [
    "index.js"
  ]
}
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   MIT License

    Copyright (c) Microsoft Corporation.

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           MIT License

Copyright (c) Sindre Sorhus <sindresorhus@gmail.com> (https://sindresorhus.com)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   {
  "name": "sumchecker",
  "version": "3.0.1",
  "author": "Mark Lee",
  "license": "Apache-2.0",
  "description": "Checksum validator",
  "main": "index.js",
  "types": "index.d.ts",
  "repository": {
    "type": "git",
    "url": "git+https://github.com/malept/sumchecker.git"
  },
  "keywords": [
    "checksum",
    "hash"
  ],
  "bugs": {
    "url": "https://github.com/malept/sumchecker/issues"
  },
  "homepage": "https://github.com/malept/sumchecker#readme",
  "engines": {
    "node": ">= 8.0"
  },
  "devDependencies": {
    "ava": "^2.2.0",
    "codecov": "^3.3.0",
    "eslint": "^6.1.0",
    "eslint-config-standard": "^14.0.0",
    "eslint-plugin-ava": "^9.0.0",
    "eslint-plugin-import": "^2.18.2",
    "eslint-plugin-node": "^10.0.0",
    "eslint-plugin-promise": "^4.0.1",
    "eslint-plugin-standard": "^4.0.0",
    "nyc": "^14.0.0",
    "tsd": "^0.11.0"
  },
  "dependencies": {
    "debug": "^4.1.0"
  },
  "scripts": {
    "ava": "ava test/index.js",
    "codecov": "nyc report --reporter=text-lcov > coverage.lcov && codecov",
    "coverage": "nyc ava test/index.js",
    "lint": "eslint .",
    "test": "npm run lint && npm run ava && npm run tsd",
    "tsd": "tsd"
  },
  "ava": {
    "babel": false,
    "compileEnhancements": false
  },
  "eslintConfig": {
    "extends": [
      "eslint:recommended",
      "plugin:ava/recommended",
      "plugin:import/errors",
      "plugin:import/warnings",
      "plugin:node/recommended",
      "plugin:promise/recommended",
      "standard"
    ],
    "plugins": [
      "ava"
    ],
    "rules": {
      "node/no-unpublished-require": [
        "error",
        {
          "allowModules": [
            "ava"
          ]
        }
      ],
      "strict": [
        "error"
      ]
    }
  }
}
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          The ISC License

Copyright (c) Isaac Z. Schlueter and Contributors

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR
IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   {
  "name": "fs-extra",
  "version": "8.1.0",
  "description": "fs-extra contains methods that aren't included in the vanilla Node.js fs package. Such as mkdir -p, cp -r, and rm -rf.",
  "engines": {
    "node": ">=6 <7 || >=8"
  },
  "homepage": "https://github.com/jprichardson/node-fs-extra",
  "repository": {
    "type": "git",
    "url": "https://github.com/jprichardson/node-fs-extra"
  },
  "keywords": [
    "fs",
    "file",
    "file system",
    "copy",
    "directory",
    "extra",
    "mkdirp",
    "mkdir",
    "mkdirs",
    "recursive",
    "json",
    "read",
    "write",
    "extra",
    "delete",
    "remove",
    "touch",
    "create",
    "text",
    "output",
    "move"
  ],
  "author": "JP Richardson <jprichardson@gmail.com>",
  "license": "MIT",
  "dependencies": {
    "graceful-fs": "^4.2.0",
    "jsonfile": "^4.0.0",
    "universalify": "^0.1.0"
  },
  "devDependencies": {
    "coveralls": "^3.0.0",
    "istanbul": "^0.4.5",
    "klaw": "^2.1.1",
    "klaw-sync": "^3.0.2",
    "minimist": "^1.1.1",
    "mocha": "^5.0.5",
    "proxyquire": "^2.0.1",
    "read-dir-files": "^0.1.1",
    "semver": "^5.3.0",
    "standard": "^12.0.1"
  },
  "main": "./lib/index.js",
  "files": [
    "lib/",
    "!lib/**/__tests__/"
  ],
  "scripts": {
    "full-ci": "npm run lint && npm run coverage",
    "coverage": "istanbul cover -i 'lib/**' -x '**/__tests__/**' test.js",
    "coveralls": "coveralls < coverage/lcov.info",
    "lint": "standard",
    "test-find": "find ./lib/**/__tests__ -name *.test.js | xargs mocha",
    "test": "npm run lint && npm run unit",
    "unit": "node test.js"
  }
}
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         MIT License

Copyright (c) Sindre Sorhus <sindresorhus@gmail.com> (sindresorhus.com)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           MIT License

Copyright (c) Sindre Sorhus <sindresorhus@gmail.com> (sindresorhus.com)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated doc