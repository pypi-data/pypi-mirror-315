/*
 * SysML 2 Pilot Implementation
 * Copyright (C) 2020  California Institute of Technology ("Caltech")
 * Copyright (C) 2020-2021  Model Driven Solutions, Inc.
 * Copyright (C) 2024  Free & Fair
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 * You should have received a copy of the GNU Lesser General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 *
 * @license LGPL-3.0-or-later <http://spdx.org/licenses/LGPL-3.0-or-later>
 */

/*
 * This version of the Jupyter syntax highlighting plugin is for
 * JupyterLab 4.0 and higher.
 *
 * Adapted by Daniel M. Zimmerman, December 2024
 */

import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { IEditorLanguageRegistry } from '@jupyterlab/codemirror';
import {
  StreamLanguage,
  LanguageSupport,
  StringStream
} from '@codemirror/language';
import { clike } from '@codemirror/legacy-modes/mode/clike';

const SYSML_MODE_NAME = 'sysml';
const SYSML_MODE_MIME = 'text/x-sysml';
const SYSML_EXTENSIONS = ['sysml'];
const SYSML_MODE_LABEL = 'SysMLv2';

const f_wordify = (h: any, s: string) => ({ ...h, [s]: true });

export function defineSysMLv2Mode(languages: IEditorLanguageRegistry): void {
  const sysmlv2 = {
    name: SYSML_MODE_NAME,
    keywords: [
      'about',
      'abstract',
      'accept',
      'action',
      'actor',
      'after',
      'alias',
      'all',
      'allocate',
      'allocation',
      'analysis',
      'and',
      'as',
      'assert',
      'assign',
      'assume',
      'at',
      'attribute',
      'bind',
      'binding',
      'by',
      'calc',
      'case',
      'comment',
      'concern',
      'connect',
      'connection',
      'constraint',
      'decide',
      'def',
      'default',
      'defined',
      'dependency',
      'derived',
      'do',
      'doc',
      'else',
      'end',
      'entry',
      'enum',
      'event',
      'exhibit',
      'exit',
      'expose',
      'filter',
      'first',
      'flow',
      'for',
      'fork',
      'frame',
      'from',
      'hastype',
      'if',
      'implies',
      'import',
      'in',
      'include',
      'individual',
      'inout',
      'interface',
      'istype',
      'item',
      'join',
      'language',
      'library',
      'locale',
      'loop',
      'merge',
      'message',
      'meta',
      'metadata',
      'nonunique',
      'not',
      'objective',
      'occurrence',
      'of',
      'or',
      'ordered',
      'out',
      'package',
      'parallel',
      'part',
      'perform',
      'port',
      'private',
      'protected',
      'public',
      'readonly',
      'redefines',
      'ref',
      'references',
      'render',
      'rendering',
      'rep',
      'require',
      'requirement',
      'return',
      'satisfy',
      'send',
      'snapshot',
      'specializes',
      'stakeholder',
      'standard',
      'state',
      'subject',
      'subsets',
      'succession',
      'terminate',
      'then',
      'timeslice',
      'to',
      'transition',
      'until',
      'use',
      'variant',
      'variation',
      'verification',
      'verify',
      'via',
      'view',
      'viewpoint',
      'when',
      'while',
      'xor'
    ].reduce(f_wordify, {}),
    defKeywords: [
      'action',
      'allocation',
      'analysis',
      'attribute',
      'binding',
      'calc',
      'case',
      'comment',
      'concern',
      'connection',
      'constraint',
      'def',
      'doc',
      'enum',
      'flow',
      'interface',
      'item',
      'metadata',
      'objective',
      'occurrence',
      'package',
      'part',
      'port',
      'ref',
      'rendering',
      'rep',
      'requirement',
      'snapshot',
      'state',
      'subject',
      'succession',
      'timeslice',
      'transition',
      'verification',
      'view',
      'viewpoint'
    ].reduce(f_wordify, {}),
    typeFirstDefinitions: true,
    atoms: ['true', 'false', 'null'].reduce(f_wordify, {}),
    number:
      /^(?:0x[a-f\d_]+|0b[01_]+|(?:[\d_]+\.?\d*|\.\d+)(?:e[-+]?[\d_]+)?)(u|ll?|l|f)?/i,
    modeProps: {
      fold: ['brace']
    },
    hooks: {
      "'": function (stream: StringStream) {
        let b_escaped = false;
        let s_next;
        while ((s_next = stream.next())) {
          if (s_next === "'" && !b_escaped) {
            break;
          }
          b_escaped = !b_escaped && s_next === '\\';
        }
        return 'variable';
      },
      '/': function (stream: StringStream) {
        if (stream.match('/*', false)) {
          stream.next();
        }
        return false;
      },
      '#': function (stream: StringStream) {
        let b_first = true;
        do {
          if (stream.match("'", true)) {
            let b_escaped = false;
            let s_next;
            while ((s_next = stream.next())) {
              if (s_next === "'" && !b_escaped) {
                break;
              }
              b_escaped = !b_escaped && s_next === '\\';
            }
          } else if (stream.match(/\w/, true)) {
            stream.eatWhile(/\w/);
          } else if (b_first) {
            return 'operator';
          }
          b_first = false;
        } while (stream.match('::', true));
        return 'keyword';
      }
    }
  };

  languages.addLanguage({
    mime: SYSML_MODE_MIME,
    name: SYSML_MODE_NAME,
    extensions: SYSML_EXTENSIONS,
    displayName: SYSML_MODE_LABEL,
    load: async () => {
      const mode = clike(sysmlv2);
      const parser = StreamLanguage.define(mode);
      const languageSupport = new LanguageSupport(parser);
      return languageSupport;
    }
  });
}

/**
 * Initialization data for extension
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab4_sysmlv2:plugin',
  description: 'JupyterLab syntax highlighting for SysMLv2',
  autoStart: true,
  requires: [IEditorLanguageRegistry],
  activate: (app: JupyterFrontEnd, languages: IEditorLanguageRegistry) => {
    defineSysMLv2Mode(languages);
  }
};

export default plugin;
