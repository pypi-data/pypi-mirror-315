"use strict";
(self["webpackChunkjupyter_cgi_theme"] = self["webpackChunkjupyter_cgi_theme"] || []).push([["lib_index_js"],{

/***/ "./lib/configuration.js":
/*!******************************!*\
  !*** ./lib/configuration.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   appConfig: () => (/* binding */ appConfig)
/* harmony export */ });
const appConfig = {
    appName: 'Insula Experiment',
    header: {
        isVisible: true,
        insulaAppsMenuLinks: [
            {
                label: 'Awareness',
                href: 'https://insula.destine.eu/advanced'
            },
            {
                label: 'Intellect',
                href: 'https://insula.destine.eu/sir'
            },
            {
                label: 'Perception',
                href: 'https://insula.destine.eu/dama'
            }
        ],
        otherInfoMenuLinks: [
            {
                label: 'Docs',
                href: 'https://platform.destine.eu/services/documents-and-api/doc/?service_name=insula'
            },
            {
                label: 'Support',
                href: 'https://platform.destine.eu/support/'
            }
        ]
    }
};


/***/ }),

/***/ "./lib/icons.js":
/*!**********************!*\
  !*** ./lib/icons.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   Icons: () => (/* binding */ Icons)
/* harmony export */ });
const Icons = {
    CGILogo: `<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="800px" height="375px" style="shape-rendering:geometricPrecision; text-rendering:geometricPrecision; image-rendering:optimizeQuality; fill-rule:evenodd; clip-rule:evenodd" xmlns:xlink="http://www.w3.org/1999/xlink"><g><path style="opacity:0.994" fill="#e11836" d="M 183.5,1.5 C 228.922,0.683531 272.089,10.0169 313,29.5C 313.833,57.506 313.667,85.506 312.5,113.5C 285.421,94.9631 255.754,82.4631 223.5,76C 175.242,68.1888 135.742,83.0221 105,120.5C 78.2883,161.493 76.6216,203.493 100,246.5C 124.154,280.919 157.487,298.919 200,300.5C 242.799,297.841 279.966,282.174 311.5,253.5C 312.833,282.167 312.833,310.833 311.5,339.5C 263.878,366.99 212.878,376.823 158.5,369C 100.368,356.537 55.8676,325.037 25,274.5C -6.56613,214.636 -6.2328,154.969 26,95.5C 56.4356,46.1741 100.269,16.0074 157.5,5C 166.292,3.65238 174.959,2.48572 183.5,1.5 Z"/></g><g><path style="opacity:0.995" fill="#e11836" d="M 526.5,1.5 C 572.643,0.467328 616.977,8.80066 659.5,26.5C 660.833,54.5 660.833,82.5 659.5,110.5C 622.781,88.7049 583.114,76.3716 540.5,73.5C 490.821,75.0669 454.654,97.7336 432,141.5C 411.692,195.439 423.526,240.939 467.5,278C 503.891,303.092 543.057,308.592 585,294.5C 585.5,272.836 585.667,251.169 585.5,229.5C 565.5,229.5 545.5,229.5 525.5,229.5C 525.5,205.833 525.5,182.167 525.5,158.5C 571.167,158.5 616.833,158.5 662.5,158.5C 662.831,221.071 662.498,283.571 661.5,346C 611.001,368.167 558.335,376.167 503.5,370C 434.842,358.113 385.342,320.946 355,258.5C 328.576,190.869 337.576,128.536 382,71.5C 420.707,28.9685 468.873,5.63518 526.5,1.5 Z"/></g><g><path style="opacity:0.997" fill="#e11837" d="M 720.5,9.5 C 746.167,9.5 771.833,9.5 797.5,9.5C 797.5,127.833 797.5,246.167 797.5,364.5C 771.833,364.5 746.167,364.5 720.5,364.5C 720.5,246.167 720.5,127.833 720.5,9.5 Z"/></g></svg>`,
    MenuIcon: `<svg viewBox="64 64 896 896" focusable="false" data-icon="menu" width="1em" height="1em" fill="currentColor" aria-hidden="true"><path d="M904 160H120c-4.4 0-8 3.6-8 8v64c0 4.4 3.6 8 8 8h784c4.4 0 8-3.6 8-8v-64c0-4.4-3.6-8-8-8zm0 624H120c-4.4 0-8 3.6-8 8v64c0 4.4 3.6 8 8 8h784c4.4 0 8-3.6 8-8v-64c0-4.4-3.6-8-8-8zm0-312H120c-4.4 0-8 3.6-8 8v64c0 4.4 3.6 8 8 8h784c4.4 0 8-3.6 8-8v-64c0-4.4-3.6-8-8-8z"></path></svg>`,
    CloseIcon: `<svg fill-rule="evenodd" viewBox="64 64 896 896" focusable="false" data-icon="close" width="1em" height="1em" fill="currentColor" aria-hidden="true"><path d="M799.86 166.31c.02 0 .04.02.08.06l57.69 57.7c.04.03.05.05.06.08a.12.12 0 010 .06c0 .03-.02.05-.06.09L569.93 512l287.7 287.7c.04.04.05.06.06.09a.12.12 0 010 .07c0 .02-.02.04-.06.08l-57.7 57.69c-.03.04-.05.05-.07.06a.12.12 0 01-.07 0c-.03 0-.05-.02-.09-.06L512 569.93l-287.7 287.7c-.04.04-.06.05-.09.06a.12.12 0 01-.07 0c-.02 0-.04-.02-.08-.06l-57.69-57.7c-.04-.03-.05-.05-.06-.07a.12.12 0 010-.07c0-.03.02-.05.06-.09L454.07 512l-287.7-287.7c-.04-.04-.05-.06-.06-.09a.12.12 0 010-.07c0-.02.02-.04.06-.08l57.7-57.69c.03-.04.05-.05.07-.06a.12.12 0 01.07 0c.03 0 .05.02.09.06L512 454.07l287.7-287.7c.04-.04.06-.05.09-.06a.12.12 0 01.07 0z"></path></svg>`,
    UserIcon: `<svg viewBox="64 64 896 896" focusable="false" data-icon="user" width="1em" height="1em" fill="currentColor" aria-hidden="true"><path d="M858.5 763.6a374 374 0 00-80.6-119.5 375.63 375.63 0 00-119.5-80.6c-.4-.2-.8-.3-1.2-.5C719.5 518 760 444.7 760 362c0-137-111-248-248-248S264 225 264 362c0 82.7 40.5 156 102.8 201.1-.4.2-.8.3-1.2.5-44.8 18.9-85 46-119.5 80.6a375.63 375.63 0 00-80.6 119.5A371.7 371.7 0 00136 901.8a8 8 0 008 8.2h60c4.4 0 7.9-3.5 8-7.8 2-77.2 33-149.5 87.8-204.3 56.7-56.7 132-87.9 212.2-87.9s155.5 31.2 212.2 87.9C779 752.7 810 825 812 902.2c.1 4.4 3.6 7.8 8 7.8h60a8 8 0 008-8.2c-1-47.8-10.9-94.3-29.5-138.2zM512 534c-45.9 0-89.1-17.9-121.6-50.4S340 407.9 340 362c0-45.9 17.9-89.1 50.4-121.6S466.1 190 512 190s89.1 17.9 121.6 50.4S684 316.1 684 362c0 45.9-17.9 89.1-50.4 121.6S557.9 534 512 534z"></path></svg>`,
    InfoIcon: `<svg viewBox="64 64 896 896" focusable="false" data-icon="info-circle" width="1em" height="1em" fill="currentColor" aria-hidden="true"><path d="M512 64C264.6 64 64 264.6 64 512s200.6 448 448 448 448-200.6 448-448S759.4 64 512 64zm0 820c-205.4 0-372-166.6-372-372s166.6-372 372-372 372 166.6 372 372-166.6 372-372 372z"></path><path d="M464 336a48 48 0 1096 0 48 48 0 10-96 0zm72 112h-48c-4.4 0-8 3.6-8 8v272c0 4.4 3.6 8 8 8h48c4.4 0 8-3.6 8-8V456c0-4.4-3.6-8-8-8z"></path></svg>`,
    AppsIcon: `<svg viewBox="64 64 896 896" focusable="false" data-icon="appstore" width="1em" height="1em" fill="currentColor" aria-hidden="true"><path d="M864 144H560c-8.8 0-16 7.2-16 16v304c0 8.8 7.2 16 16 16h304c8.8 0 16-7.2 16-16V160c0-8.8-7.2-16-16-16zm0 400H560c-8.8 0-16 7.2-16 16v304c0 8.8 7.2 16 16 16h304c8.8 0 16-7.2 16-16V560c0-8.8-7.2-16-16-16zM464 144H160c-8.8 0-16 7.2-16 16v304c0 8.8 7.2 16 16 16h304c8.8 0 16-7.2 16-16V160c0-8.8-7.2-16-16-16zm0 400H160c-8.8 0-16 7.2-16 16v304c0 8.8 7.2 16 16 16h304c8.8 0 16-7.2 16-16V560c0-8.8-7.2-16-16-16z"></path></svg>`
};


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _configuration__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./configuration */ "./lib/configuration.js");
/* harmony import */ var _pallettes__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./pallettes */ "./lib/pallettes/light-pallette-setter.js");
/* harmony import */ var _pallettes__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./pallettes */ "./lib/pallettes/dark-pallette-setter.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./utils */ "./lib/utils.js");
/* harmony import */ var _style_favicon_png__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../style/favicon.png */ "./style/favicon.png");





(0,_utils__WEBPACK_IMPORTED_MODULE_1__.initiAppFaviconAndTitle)(_configuration__WEBPACK_IMPORTED_MODULE_2__.appConfig.appName, _style_favicon_png__WEBPACK_IMPORTED_MODULE_3__);
/**
 * Initialization data for the jupyter-cgi-theme extension.
 */
const plugin = {
    id: 'jupyter-cgi-theme:plugin',
    description: 'The Jupyter CGI theme',
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.IThemeManager],
    activate: (app, manager) => {
        app.started.then(() => {
            if (_configuration__WEBPACK_IMPORTED_MODULE_2__.appConfig.header.isVisible) {
                (0,_utils__WEBPACK_IMPORTED_MODULE_1__.initAppHeader)();
            }
        });
        /**
         * Due to the current limitation of not being able to register multiple themes
         * [https://github.com/jupyterlab/jupyterlab/issues/14202]
         * in the same extension when each theme has its own separate CSS file, we
         * handle theme variants by storing the color palette in TypeScript files and
         * loading them dynamically through a script. This approach allows us to load
         * a base theme ('jupyter-cgi-theme/index.css') and then override the necessary color properties
         * based on the selected palette.
         *
         * * Note: In development mode, the path to 'index.css' might differ because the plugin
         * expects the CSS file to be located in the mounted app's root folder (lib).
         */
        const pallettesSetters = [_pallettes__WEBPACK_IMPORTED_MODULE_4__.LightPalletteSetter, _pallettes__WEBPACK_IMPORTED_MODULE_5__.DarkPalletteSetter];
        const baseTheme = 'jupyter-cgi-theme/index.css';
        pallettesSetters.forEach(Pallette => {
            const pallette = new Pallette();
            manager.register({
                name: pallette.name,
                isLight: pallette.type === 'light',
                load: () => {
                    pallette.setColorPallette();
                    return manager.loadCSS(baseTheme);
                },
                unload: () => Promise.resolve(undefined)
            });
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/pallettes/dark-pallette-setter.js":
/*!***********************************************!*\
  !*** ./lib/pallettes/dark-pallette-setter.js ***!
  \***********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   DarkPalletteSetter: () => (/* binding */ DarkPalletteSetter)
/* harmony export */ });
class DarkPalletteSetter {
    constructor() {
        this.name = 'CGI Theme Dark';
        this.type = 'dark';
    }
    setColorPallette() {
        /**
         * Borders
         */
        document.documentElement.style.setProperty('--jp-border-color0', 'var(--md-grey-200)');
        document.documentElement.style.setProperty('--jp-border-color1', 'var(--md-grey-300)');
        document.documentElement.style.setProperty('--jp-border-color2', 'var(--md-grey-400)');
        document.documentElement.style.setProperty('--jp-border-color3', 'var(--md-grey-400)');
        /**
         * Defaults use Material Design specification
         */
        document.documentElement.style.setProperty('--jp-ui-font-color0', 'rgba(255, 255, 255, 1)');
        document.documentElement.style.setProperty('--jp-ui-font-color1', 'rgba(255, 255, 255, 1)');
        document.documentElement.style.setProperty('--jp-ui-font-color2', 'rgba(255, 255, 255, 0.9)');
        document.documentElement.style.setProperty('--jp-ui-font-color3', 'rgba(255, 255, 255, 0.8)');
        /**
         * Defaults use Material Design specification
         */
        document.documentElement.style.setProperty('--jp-content-font-color0', 'rgba(255, 255, 255, 1)');
        document.documentElement.style.setProperty('--jp-content-font-color1', 'rgba(255, 255, 255, 0.9)');
        document.documentElement.style.setProperty('--jp-content-font-color2', 'rgba(255, 255, 255, 0.8)');
        document.documentElement.style.setProperty('--jp-content-font-color3', 'rgba(255, 255, 255, 0.8)');
        /**
         * Layout
         */
        document.documentElement.style.setProperty('--jp-layout-color0', '#1f1f1f');
        document.documentElement.style.setProperty('--jp-layout-color1', '#1f1f1f');
        document.documentElement.style.setProperty('--jp-layout-color2', '#4d4d4d');
        document.documentElement.style.setProperty('--jp-layout-color3', '#4d4d4d');
        document.documentElement.style.setProperty('--jp-layout-color4', '#4d4d4d');
        /**
         * Inverse Layout
         */
        document.documentElement.style.setProperty('--jp-inverse-layout-color0', 'rgb(255, 255, 255)');
        document.documentElement.style.setProperty('--jp-inverse-layout-color1', 'rgb(255, 255, 255)');
        document.documentElement.style.setProperty('--jp-inverse-layout-color2', 'rgba(255, 255, 255, 0.87)');
        document.documentElement.style.setProperty('--jp-inverse-layout-color3', 'rgba(255, 255, 255, 0.87)');
        document.documentElement.style.setProperty('--jp-inverse-layout-color4', 'rgba(255, 255, 255, 0.87)');
        /**
         * State colors (warn, error, success, info)
         */
        document.documentElement.style.setProperty('--jp-warn-color0', 'var(--md-purple-700)');
        document.documentElement.style.setProperty('--jp-warn-color1', 'var(--md-purple-500)');
        document.documentElement.style.setProperty('--jp-warn-color2', 'var(--md-purple-300)');
        document.documentElement.style.setProperty('--jp-warn-color3', 'var(--md-purple-100)');
        /**
         * Cell specific styles
         */
        document.documentElement.style.setProperty('--jp-cell-editor-background', '#0D1527');
        document.documentElement.style.setProperty('--jp-cell-prompt-not-active-font-color', 'var(--md-grey-200)');
        /**
         * Rendermime styles
         */
        document.documentElement.style.setProperty('--jp-rendermime-error-background', '#0D1527');
        document.documentElement.style.setProperty('--jp-rendermime-table-row-background', 'var(--md-grey-800)');
        document.documentElement.style.setProperty('--jp-rendermime-table-row-hover-background', 'var(--md-grey-700)');
        /**
         * Code mirror specific styles
         */
        document.documentElement.style.setProperty('--jp-mirror-editor-operator-color', '#a2f');
        document.documentElement.style.setProperty('--jp-mirror-editor-meta-color', '#a2f');
        document.documentElement.style.setProperty('--jp-mirror-editor-attribute-color', 'rgb(255, 255, 255)');
    }
}


/***/ }),

/***/ "./lib/pallettes/light-pallette-setter.js":
/*!************************************************!*\
  !*** ./lib/pallettes/light-pallette-setter.js ***!
  \************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   LightPalletteSetter: () => (/* binding */ LightPalletteSetter)
/* harmony export */ });
class LightPalletteSetter {
    constructor() {
        this.name = 'CGI Theme Light';
        this.type = 'light';
    }
    setColorPallette() {
        /**
         * Borders
         */
        document.documentElement.style.setProperty('--jp-border-color0', 'var(--md-grey-400)');
        document.documentElement.style.setProperty('--jp-border-color1', 'var(--md-grey-400)');
        document.documentElement.style.setProperty('--jp-border-color2', 'var(--md-grey-300)');
        document.documentElement.style.setProperty('--jp-border-color3', 'var(--md-grey-200)');
        /**
         * Defaults use Material Design specification
         */
        document.documentElement.style.setProperty('--jp-ui-font-color0', 'rgba(0, 0, 0, 1)');
        document.documentElement.style.setProperty('--jp-ui-font-color1', 'rgba(0, 0, 0, 0.87)');
        document.documentElement.style.setProperty('--jp-ui-font-color2', 'rgba(0, 0, 0, 0.54)');
        document.documentElement.style.setProperty('--jp-ui-font-color3', 'rgba(0, 0, 0, 0.38)');
        /**
         * Defaults use Material Design specification
         */
        document.documentElement.style.setProperty('--jp-content-font-color0', 'rgba(0, 0, 0, 1)');
        document.documentElement.style.setProperty('--jp-content-font-color1', 'rgba(0, 0, 0, 0.87)');
        document.documentElement.style.setProperty('--jp-content-font-color2', 'rgba(0, 0, 0, 0.54)');
        document.documentElement.style.setProperty('--jp-content-font-color3', 'rgba(0, 0, 0, 0.38)');
        /**
         * Layout
         */
        document.documentElement.style.setProperty('--jp-layout-color0', 'white');
        document.documentElement.style.setProperty('--jp-layout-color1', 'white');
        document.documentElement.style.setProperty('--jp-layout-color2', 'var(--md-grey-200)');
        document.documentElement.style.setProperty('--jp-layout-color3', '#7B34DB');
        document.documentElement.style.setProperty('--jp-layout-color4', 'var(--md-grey-600)');
        /**
         * Inverse Layout
         */
        document.documentElement.style.setProperty('--jp-inverse-layout-color0', '#111111');
        document.documentElement.style.setProperty('--jp-inverse-layout-color1', 'var(--md-grey-900)');
        document.documentElement.style.setProperty('--jp-inverse-layout-color2', 'var(--md-grey-800)');
        document.documentElement.style.setProperty('--jp-inverse-layout-color3', 'var(--md-grey-700)');
        document.documentElement.style.setProperty('--jp-inverse-layout-color4', 'var(--md-grey-600)');
        /**
         * State colors (warn, error, success, info)
         */
        document.documentElement.style.setProperty('--jp-warn-color0', 'var(--md-purple-700)');
        document.documentElement.style.setProperty('--jp-warn-color1', 'var(--md-purple-500)');
        document.documentElement.style.setProperty('--jp-warn-color2', 'var(--md-purple-300)');
        document.documentElement.style.setProperty('--jp-warn-color3', 'var(--md-purple-100)');
        /**
         * Cell specific styles
         */
        document.documentElement.style.setProperty('--jp-cell-editor-background', 'var(--md-grey-100)');
        document.documentElement.style.setProperty('--jp-cell-prompt-not-active-font-color', 'var(--md-grey-700)');
        /**
         * Rendermime styles
         */
        document.documentElement.style.setProperty('--jp-rendermime-error-background', '#fdd');
        document.documentElement.style.setProperty('--jp-rendermime-table-row-background', 'var(--md-grey-100)');
        document.documentElement.style.setProperty('--jp-rendermime-table-row-hover-background', 'var(--md-grey-200)');
        /**
         * Code mirror specific styles
         */
        document.documentElement.style.setProperty('--jp-mirror-editor-operator-color', '#aa22ff');
        document.documentElement.style.setProperty('--jp-mirror-editor-meta-color', '#aa22ff');
        document.documentElement.style.setProperty('--jp-mirror-editor-attribute-color', '#00c');
    }
}


/***/ }),

/***/ "./lib/utils.js":
/*!**********************!*\
  !*** ./lib/utils.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   createLogo: () => (/* binding */ createLogo),
/* harmony export */   initAppHeader: () => (/* binding */ initAppHeader),
/* harmony export */   initAppLogo: () => (/* binding */ initAppLogo),
/* harmony export */   initiAppFaviconAndTitle: () => (/* binding */ initiAppFaviconAndTitle)
/* harmony export */ });
/* harmony import */ var _configuration__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./configuration */ "./lib/configuration.js");
/* harmony import */ var _icons__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./icons */ "./lib/icons.js");
/* harmony import */ var _style_apple_touch_icon_png__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../style/apple-touch-icon.png */ "./style/apple-touch-icon.png");
/* harmony import */ var _style_logo_png__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../style/logo.png */ "./style/logo.png");




/**
 * Creates a logo, consisting of an 'img' element wrapped inside an 'a' (anchor) element.
 *
 * @param src - The media source URL for the img element.
 * @param alt - The alt text for the img element.
 * @param href - The URL the anchor element should link to (optional).
 * @returns {HTMLAnchorElement} - The anchor element containing the logo image.
 */
const createLogo = (src, alt, href) => {
    const logoAnchorEl = document.createElement('a');
    logoAnchorEl.href = href || '#';
    logoAnchorEl.target = '_blank';
    const logoImgEl = document.createElement('img');
    logoImgEl.src = src;
    logoImgEl.alt = alt;
    logoAnchorEl.appendChild(logoImgEl);
    return logoAnchorEl;
};
/**
 * Overrides the default document title and favicon.
 *
 * @param {string} title - The application title to set.
 * @param {string} faviconSource - The URL or path for the application favicon.
 */
const initiAppFaviconAndTitle = (title, faviconSource) => {
    const head = document.head;
    const iconLinks = head.querySelectorAll('link[rel="icon"]');
    const shortcutIconLinks = head.querySelectorAll('link[rel="shortcut icon"]');
    const appleTouchIconLinks = head.querySelectorAll('link[rel="apple-touch-icon"]');
    const busyIconLinks = head.querySelectorAll('link[type="image/x-icon"]');
    // Existent favicons set by JupyterLab
    [
        ...Array.from(iconLinks),
        ...Array.from(shortcutIconLinks),
        ...Array.from(appleTouchIconLinks),
        ...Array.from(busyIconLinks)
    ].forEach(favicon => {
        if (head.contains(favicon)) {
            head.removeChild(favicon);
        }
    });
    const linkIcon = document.createElement('link');
    linkIcon.rel = 'icon';
    linkIcon.type = 'image/png';
    linkIcon.href = faviconSource;
    linkIcon.setAttribute('sizes', '32x32');
    head.appendChild(linkIcon);
    const linkShortCut = document.createElement('link');
    linkShortCut.rel = 'shortcut icon';
    linkShortCut.type = 'image/png';
    linkShortCut.href = faviconSource;
    linkShortCut.setAttribute('sizes', '32x32');
    head.appendChild(linkShortCut);
    const linkAppleTouch = document.createElement('link');
    linkAppleTouch.rel = 'apple-touch-icon';
    linkAppleTouch.href = _style_apple_touch_icon_png__WEBPACK_IMPORTED_MODULE_0__;
    linkAppleTouch.setAttribute('sizes', '180x180');
    head.appendChild(linkAppleTouch);
    const svgDataUrl = `data:image/svg+xml;charset=utf-8,${encodeURIComponent(_icons__WEBPACK_IMPORTED_MODULE_1__.Icons.CGILogo)}`;
    const linkMaskIcon = document.createElement('link');
    linkMaskIcon.rel = 'mask-icon';
    linkMaskIcon.type = 'image/svg+xml';
    linkMaskIcon.color = '#7b34db';
    linkMaskIcon.href = svgDataUrl;
    head.appendChild(linkMaskIcon);
    Object.defineProperty(document, 'title', {
        set(_arg) {
            var _a, _b;
            (_b = (_a = Object.getOwnPropertyDescriptor(Document.prototype, 'title'
            // Edit the document.title property setter,
            // call the original setter function for document.title and make sure 'this' is set to the document object,
            // then overrides the value to set
            )) === null || _a === void 0 ? void 0 : _a.set) === null || _b === void 0 ? void 0 : _b.call(document, title);
        },
        configurable: true
    });
};
/**
 * Initializes the application header by adding various elements.
 */
const initAppHeader = () => {
    initAppLogo();
    try {
        const userData = localStorage.getItem('@jupyterlab/services:UserManager#user');
        if (userData) {
            const user = JSON.parse(userData);
            if (user && user.name) {
                const headerContainerEl = document.createElement('div');
                headerContainerEl.classList.add('desp-header-container');
                headerContainerEl.id = 'desp-header-container';
                /** Create the icons */
                const iconsContainerEl = document.createElement('div');
                iconsContainerEl.classList.add('desp-header-icons');
                const icon1 = document.createElement('span');
                icon1.innerHTML = _icons__WEBPACK_IMPORTED_MODULE_1__.Icons.AppsIcon;
                icon1.id = 'insulaAppsMenuLinks';
                icon1.addEventListener('click', () => {
                    showHeaderMenu(_configuration__WEBPACK_IMPORTED_MODULE_2__.appConfig.header.insulaAppsMenuLinks, icon1.id, true);
                });
                const icon2 = document.createElement('span');
                icon2.innerHTML = _icons__WEBPACK_IMPORTED_MODULE_1__.Icons.InfoIcon;
                icon2.id = 'otherInfoMenuLinks';
                icon2.addEventListener('click', () => {
                    showHeaderMenu(_configuration__WEBPACK_IMPORTED_MODULE_2__.appConfig.header.otherInfoMenuLinks, icon2.id, false);
                });
                iconsContainerEl.appendChild(icon1);
                iconsContainerEl.appendChild(icon2);
                headerContainerEl.appendChild(iconsContainerEl);
                /** Create the user name panel */
                const userNameContainerEl = document.createElement('div');
                userNameContainerEl.classList.add('desp-header-user');
                const iconEl = document.createElement('span');
                iconEl.innerHTML = _icons__WEBPACK_IMPORTED_MODULE_1__.Icons.UserIcon;
                const spanEl = document.createElement('span');
                spanEl.innerText = user.name;
                userNameContainerEl.appendChild(iconEl);
                userNameContainerEl.appendChild(spanEl);
                headerContainerEl.appendChild(userNameContainerEl);
                document.body.appendChild(headerContainerEl);
            }
        }
    }
    catch (error) {
        console.error('Error parsing user data:', error);
    }
};
/**
 * Adds a custom logo to the application.
 */
const initAppLogo = () => {
    const imgEl = document.createElement('img');
    imgEl.alt = 'Destination Earth Logo';
    imgEl.src = _style_logo_png__WEBPACK_IMPORTED_MODULE_3__;
    const logoSectionEL = [
        document.getElementById('jp-MainLogo'),
        document.getElementById('jp-RetroLogo')
    ];
    // Append the logo image and text to each logo section
    logoSectionEL.forEach(el => {
        if (el) {
            el.appendChild(imgEl);
            const spanEl = document.createElement('span');
            spanEl.classList.add('jp-MainLogo-span');
            spanEl.innerHTML = 'Insula Experiment';
            el.appendChild(spanEl);
        }
    });
};
let currentOpenMenuId = '';
/**
 * Mounts or toggles the visibility of the header menu.
 *
 * @param links - The links to display in the menu.
 * @param id - An ID to identify the menu element.
 * @param avatar - If true, an avatar will be displayed next to each link.
 */
const showHeaderMenu = (links, id, avatar) => {
    const headerMenuContainerId = `desp-header-menu-container-${id}`;
    let headerMenuContainerEl = document.getElementById(headerMenuContainerId);
    // Hide the currently open menu if it's different from the one being toggled
    if (currentOpenMenuId && currentOpenMenuId !== headerMenuContainerId) {
        const currentMenuEl = document.getElementById(currentOpenMenuId);
        if (currentMenuEl) {
            currentMenuEl.style.display = 'none';
        }
    }
    if (headerMenuContainerEl) {
        // Toggle visibility of the existing menu
        if (headerMenuContainerEl.style.display === 'block') {
            headerMenuContainerEl.style.display = 'none';
            currentOpenMenuId = '';
        }
        else {
            headerMenuContainerEl.style.display = 'block';
            currentOpenMenuId = headerMenuContainerId;
        }
    }
    else {
        // Create the menu container if it doesn't exist
        headerMenuContainerEl = document.createElement('div');
        headerMenuContainerEl.id = headerMenuContainerId;
        headerMenuContainerEl.classList.add('desp-header-menu-container');
        const ulEl = document.createElement('ul');
        ulEl.classList.add('desp-footer-menu-ul');
        links.forEach(link => {
            const liEl = document.createElement('li');
            const anchorEl = document.createElement('a');
            anchorEl.href = link.href;
            anchorEl.target = '_blank';
            anchorEl.innerText = link.label;
            liEl.appendChild(anchorEl);
            if (avatar) {
                const avatarLetter = link.label.charAt(0).toUpperCase();
                const spanEl = document.createElement('div');
                spanEl.innerText = avatarLetter;
                spanEl.classList.add('desp-header-menu-avatar');
                anchorEl.before(spanEl);
            }
            ulEl.appendChild(liEl);
        });
        if (id === 'insulaAppsMenuLinks') {
            const paragraphEl = document.createElement('p');
            paragraphEl.innerText = 'Other Insula Applications';
            headerMenuContainerEl.appendChild(paragraphEl);
        }
        headerMenuContainerEl.appendChild(ulEl);
        const menuButtonEl = document.getElementById(id);
        if (id === 'insulaAppsMenuLinks' && menuButtonEl) {
            headerMenuContainerEl.style.transform = 'translateX(-50px)';
        }
        menuButtonEl === null || menuButtonEl === void 0 ? void 0 : menuButtonEl.before(headerMenuContainerEl);
        currentOpenMenuId = headerMenuContainerId;
    }
};
document.addEventListener('mouseover', event => {
    var _a;
    if (currentOpenMenuId) {
        const menuDivEl = document.getElementById(currentOpenMenuId);
        if (menuDivEl && menuDivEl.style.display !== 'none') {
            if (!menuDivEl.contains(event.target) &&
                !((_a = document
                    .getElementById('desp-header-container')) === null || _a === void 0 ? void 0 : _a.contains(event.target))) {
                menuDivEl.style.display = 'none';
                currentOpenMenuId = '';
            }
        }
    }
});


/***/ }),

/***/ "./style/apple-touch-icon.png":
/*!************************************!*\
  !*** ./style/apple-touch-icon.png ***!
  \************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

module.exports = __webpack_require__.p + "5ba9f5de2a2d0be07dd0.png";

/***/ }),

/***/ "./style/favicon.png":
/*!***************************!*\
  !*** ./style/favicon.png ***!
  \***************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

module.exports = __webpack_require__.p + "2714a8345c85e5efab18.png";

/***/ }),

/***/ "./style/logo.png":
/*!************************!*\
  !*** ./style/logo.png ***!
  \************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

module.exports = __webpack_require__.p + "5ba9f5de2a2d0be07dd0.png";

/***/ })

}]);
//# sourceMappingURL=lib_index_js.1b9a11b7a223083bc29d.js.map