;(function( root ) {

/**
 * Application global object.
 * @namespace joms
 */
if ( typeof root.joms !== 'object' ) {
    root.joms = {};
}

/**
 * Debug flag.
 * @name joms.DEBUG
 * @const {boolean}
 */
root.joms.DEBUG = false; // @@release@@root.joms.DEBUG = false;@@

/**
 * Application logger.
 * @function joms.log
 * @param {mixed} data
 */
root.joms.log = root.joms.info = root.joms.warn = function( data ) {
    if ( root.joms.DEBUG && root.console && root.console.log ) { // @@release@@@@
        root.console.log( 'JOMS: ', data ); // @@release@@@@
    } // @@release@@@@
};

// Temporary variables to reserve some current application libraries in case of override.
root.joms_cache_$LAB = root.$LAB;
root.joms_cache_Hammer = root.Hammer;

})( this );

/*! LAB.js v2.0.3 | (c) Kyle Simpson | MIT license */
(function(o){var K=o.$LAB,y="UseLocalXHR",z="AlwaysPreserveOrder",u="AllowDuplicates",A="CacheBust",B="BasePath",C=/^[^?#]*\//.exec(location.href)[0],D=/^\w+\:\/\/\/?[^\/]+/.exec(C)[0],i=document.head||document.getElementsByTagName("head"),L=(o.opera&&Object.prototype.toString.call(o.opera)=="[object Opera]")||("MozAppearance"in document.documentElement.style),q=document.createElement("script"),E=typeof q.preload=="boolean",r=E||(q.readyState&&q.readyState=="uninitialized"),F=!r&&q.async===true,M=!r&&!F&&!L;function G(a){return Object.prototype.toString.call(a)=="[object Function]"}function H(a){return Object.prototype.toString.call(a)=="[object Array]"}function N(a,c){var b=/^\w+\:\/\//;if(/^\/\/\/?/.test(a)){a=location.protocol+a}else if(!b.test(a)&&a.charAt(0)!="/"){a=(c||"")+a}return b.test(a)?a:((a.charAt(0)=="/"?D:C)+a)}function s(a,c){for(var b in a){if(a.hasOwnProperty(b)){c[b]=a[b]}}return c}function O(a){var c=false;for(var b=0;b<a.scripts.length;b++){if(a.scripts[b].ready&&a.scripts[b].exec_trigger){c=true;a.scripts[b].exec_trigger();a.scripts[b].exec_trigger=null}}return c}function t(a,c,b,d){a.onload=a.onreadystatechange=function(){if((a.readyState&&a.readyState!="complete"&&a.readyState!="loaded")||c[b])return;a.onload=a.onreadystatechange=null;d()}}function I(a){a.ready=a.finished=true;for(var c=0;c<a.finished_listeners.length;c++){a.finished_listeners[c]()}a.ready_listeners=[];a.finished_listeners=[]}function P(d,f,e,g,h){setTimeout(function(){var a,c=f.real_src,b;if("item"in i){if(!i[0]){setTimeout(arguments.callee,25);return}i=i[0]}a=document.createElement("script");if(f.type)a.type=f.type;if(f.charset)a.charset=f.charset;if(h){if(r){e.elem=a;if(E){a.preload=true;a.onpreload=g}else{a.onreadystatechange=function(){if(a.readyState=="loaded")g()}}a.src=c}else if(h&&c.indexOf(D)==0&&d[y]){b=new XMLHttpRequest();b.onreadystatechange=function(){if(b.readyState==4){b.onreadystatechange=function(){};e.text=b.responseText+"\n//@ sourceURL="+c;g()}};b.open("GET",c);b.send()}else{a.type="text/cache-script";t(a,e,"ready",function(){i.removeChild(a);g()});a.src=c;i.insertBefore(a,i.firstChild)}}else if(F){a.async=false;t(a,e,"finished",g);a.src=c;i.insertBefore(a,i.firstChild)}else{t(a,e,"finished",g);a.src=c;i.insertBefore(a,i.firstChild)}},0)}function J(){var l={},Q=r||M,n=[],p={},m;l[y]=true;l[z]=false;l[u]=false;l[A]=false;l[B]="";function R(a,c,b){var d;function f(){if(d!=null){d=null;I(b)}}if(p[c.src].finished)return;if(!a[u])p[c.src].finished=true;d=b.elem||document.createElement("script");if(c.type)d.type=c.type;if(c.charset)d.charset=c.charset;t(d,b,"finished",f);if(b.elem){b.elem=null}else if(b.text){d.onload=d.onreadystatechange=null;d.text=b.text}else{d.src=c.real_src}i.insertBefore(d,i.firstChild);if(b.text){f()}}function S(c,b,d,f){var e,g,h=function(){b.ready_cb(b,function(){R(c,b,e)})},j=function(){b.finished_cb(b,d)};b.src=N(b.src,c[B]);b.real_src=b.src+(c[A]?((/\?.*$/.test(b.src)?"&_":"?_")+~~(Math.random()*1E9)+"="):"");if(!p[b.src])p[b.src]={items:[],finished:false};g=p[b.src].items;if(c[u]||g.length==0){e=g[g.length]={ready:false,finished:false,ready_listeners:[h],finished_listeners:[j]};P(c,b,e,((f)?function(){e.ready=true;for(var a=0;a<e.ready_listeners.length;a++){e.ready_listeners[a]()}e.ready_listeners=[]}:function(){I(e)}),f)}else{e=g[0];if(e.finished){j()}else{e.finished_listeners.push(j)}}}function v(){var e,g=s(l,{}),h=[],j=0,w=false,k;function T(a,c){a.ready=true;a.exec_trigger=c;x()}function U(a,c){a.ready=a.finished=true;a.exec_trigger=null;for(var b=0;b<c.scripts.length;b++){if(!c.scripts[b].finished)return}c.finished=true;x()}function x(){while(j<h.length){if(G(h[j])){try{h[j++]()}catch(err){}continue}else if(!h[j].finished){if(O(h[j]))continue;break}j++}if(j==h.length){w=false;k=false}}function V(){if(!k||!k.scripts){h.push(k={scripts:[],finished:true})}}e={script:function(){for(var f=0;f<arguments.length;f++){(function(a,c){var b;if(!H(a)){c=[a]}for(var d=0;d<c.length;d++){V();a=c[d];if(G(a))a=a();if(!a)continue;if(H(a)){b=[].slice.call(a);b.unshift(d,1);[].splice.apply(c,b);d--;continue}if(typeof a=="string")a={src:a};a=s(a,{ready:false,ready_cb:T,finished:false,finished_cb:U});k.finished=false;k.scripts.push(a);S(g,a,k,(Q&&w));w=true;if(g[z])e.wait()}})(arguments[f],arguments[f])}return e},wait:function(){if(arguments.length>0){for(var a=0;a<arguments.length;a++){h.push(arguments[a])}k=h[h.length-1]}else k=false;x();return e}};return{script:e.script,wait:e.wait,setOptions:function(a){s(a,g);return e}}}m={setGlobalDefaults:function(a){s(a,l);return m},setOptions:function(){return v().setOptions.apply(null,arguments)},script:function(){return v().script.apply(null,arguments)},wait:function(){return v().wait.apply(null,arguments)},queueScript:function(){n[n.length]={type:"script",args:[].slice.call(arguments)};return m},queueWait:function(){n[n.length]={type:"wait",args:[].slice.call(arguments)};return m},runQueue:function(){var a=m,c=n.length,b=c,d;for(;--b>=0;){d=n.shift();a=a[d.type].apply(null,d.args)}return a},noConflict:function(){o.$LAB=K;return m},sandbox:function(){return J()}};return m}o.$LAB=J();(function(a,c,b){if(document.readyState==null&&document[a]){document.readyState="loading";document[a](c,b=function(){document.removeEventListener(c,b,false);document.readyState="complete"},false)}})("addEventListener","DOMContentLoaded")})(this);

;(function( root, undef ) {

/**
 * Cache $LAB.js instance.
 * @type {object} joms.$LAB - Local copy of $LAB.js.
 */
root.joms.$LAB = root.$LAB;
root.$LAB = root.joms_cache_$LAB;
delete root.joms_cache_$LAB;

/**
 * Cache jQuery instance.
 * @type {object} joms.jQuery
 */
root.joms.jQuery = undef;

/**
 * Cache Hammer.js instance.
 * @type {object} joms.Hammer
 */
root.joms.Hammer = undef;

/**
 * Cache Underscore.js instance.
 * @type {object} joms._
 */
root.joms._ = undef;

/**
 * Cache Backbone.js instance.
 * @type {object} joms.Backbone
 */
root.joms.Backbone = undef;

/**
 * Attach additional ajax response.
 * @function joms.onAjaxReponse
 * @param {function}
 */
root.joms.onAjaxReponse = function( id, callback ) {
    if ( !root.joms._onAjaxReponseQueue ) root.joms._onAjaxReponseQueue = [];
    if ( !root.joms._onAjaxReponseQueue[ id ] ) root.joms._onAjaxReponseQueue[ id ] = [];
    root.joms._onAjaxReponseQueue[ id ].push( callback );
};

/**
 * Attach function to trigger when application is starting.
 * @function joms.onStart
 * @param {function}
 */
root.joms.onStart = function( fn ) {
    if ( root.joms._onStartQueue === undef ) root.joms._onStartQueue = [];
    if ( root.joms._onStartStarted ) fn( root.joms.jQuery );
    else root.joms._onStartQueue.push( fn );
};

/**
 * Triggers start application.
 * @function joms.start
 */
root.joms.start = function() {
    if ( root.joms_queue && root.joms_queue.length ) {
        if ( root.joms._onStartQueue === undef ) root.joms._onStartQueue = [];
        root.joms._onStartQueue = root.joms_queue.concat( root.joms._onStartQueue );
        root.joms_queue = [];
    }

    if ( root.joms._onStartQueue !== undef ) {
        while ( root.joms._onStartQueue.length ) {
            try {
                ( root.joms._onStartQueue.shift() )( root.joms.jQuery );
            } catch (e) {}
        }
    }

    root.joms._onStartStarted = true;
};

/**
 * Fix some ui quirks which cannot be handled with PHP or CSS.
 * @todo Should be moved elsewhere instead of in loader.js
 * @function joms.fixUI
 */
root.joms.fixUI = function() {

    // Remove empty module wrappers.
    var tabbed = document.getElementsByClassName('joms-module__wrapper'),
        stacked = document.getElementsByClassName('joms-module__wrapper--stacked'),
        sidebar, main, mobile, cname, i;

    for ( i = tabbed.length - 1; i >= 0; i-- ) {
        if ( ! tabbed[i].innerHTML.match(/joms-tab__content|joms-js--app-new/) ) {
            tabbed[i].parentNode.removeChild( tabbed[i] );
        }
    }

    for ( i = stacked.length - 1; i >= 0; i-- ) {
        if ( ! stacked[i].innerHTML.match(/joms-module--stacked|joms-js--app-new/) ) {
            stacked[i].parentNode.removeChild( stacked[i] );
        }
    }

    // Remove sidebar if no modules there.
    sidebar = document.getElementsByClassName('joms-sidebar')[0];
    if ( sidebar && ( ! sidebar.innerHTML.match(/joms-module|app-position/) ) ) {
        main = document.getElementsByClassName('joms-main')[0];
        sidebar.parentNode.removeChild( sidebar );
        if ( main ) {
            main.className += ' joms-main--full';
        }
    }

    // Assumes non-touchable for non-mobile browsers.
    mobile = /android|webos|iphone|ipad|ipod|blackberry|iemobile|opera mini/i;
    if ( !mobile.test( navigator.userAgent ) ) {
        cname = document.documentElement.className || '';
        document.documentElement.className = cname + (cname.length ? ' ' : '') + 'joms-no-touch';
    }

    // Needs to add wrapper to .joms-select.
    joms.onStart(function( $ ) {
        $(function() {
            $('.joms-select').each(function() {
                var el = $(this),
                    multiple;

                if ( !el.parent('.joms-select--wrapper').length ) {
                    multiple = el.attr('size') || el.attr('multiple');
                    el.wrap( '<div class="joms-select--wrapper' + (multiple ? ' joms-select--expand' : '') + '"></div>' );
                }
            });
        });
        
        if (location.href.includes("oauth_verifier") && location.href.includes("twitterlogin")){joms.api.fbcUpdate();}
        else if (location.href.includes("linkedincode")) {joms.api.fbcUpdate();}
        else if (location.href.includes("googleid")) {joms.api.fbcUpdate();}
    });
};

root.joms.ie  = !!navigator.userAgent.match(/Trident.*rv\:11\./); // joms only support ie 11

var getOptions = root.Joomla && root.Joomla.getOptions,
    DATA;

// Retrieve all data and language translations.
DATA = getOptions && getOptions( 'com_community' ) || (root.joms_data || {});

// Deprecated!
root.joms_lang = DATA.translations || {};

// Data getter.
root.joms.getData = function( key ) {
    return DATA[ key ];
}

root.joms.getLayout = function( key ) {
    var layouts = DATA.layouts || {};
    return layouts[key];
}

// FROM THIS POINT BELOW IS A JOMSOCIAL JAVASCRIPT LOADING SEQUENCE!

// Path mapper.
var path_source  = 'source/js/',
    path_release = 'release/js/',
    path_vendors = 'vendors/',
    path_jquery  = path_vendors + 'jquery.min.js',
    path_require = path_vendors + 'require.min.js',
    path_bundle  = 'bundle.js';

// Loading sequence.
function load() {
    var isdev = root.joms.DEBUG,
        relpath = root.joms_assets_url || '',
        relpath_bundle = relpath + ( isdev ? path_source : path_release ) + path_bundle;

    root.joms.$LAB
        // Load jQuery.
        .script(function() { return root.jQuery ? null : ( relpath + path_jquery ); })
        .wait(function() { root.joms_init_toolkit(); })
        .wait( postLoad )
        // Load RequireJS on development environment.
        .script(function() { return isdev ? ( relpath + path_require ) : null; })
        .wait(function() { isdev && require.config({ baseUrl: relpath + path_source }); })
        // Load bundled script.
        .script( relpath_bundle )
      
        // Load legacy scripts.
        .wait(function() {
            root.joms_init_postbox();
            root.joms.misc.view.fixSVG();
           
        });
}

// Post-loading initialization.
function postLoad() {
    root.joms.jQuery = root.jQuery;
    root.joms.loadCSS = root.loadCSS;

    root.joms.Hammer = root.Hammer;
    root.Hammer = root.joms_cache_Hammer;
    delete root.joms_cache_Hammer;

    root.joms._ = root._; // .noConflict();
    root.joms.Backbone = root.Backbone.noConflict();
    root.joms.Backbone.$ = root.joms.jQuery;
}

// EXECUTE LOADING SEQUENCE!

document.addEventListener("DOMContentLoaded", function() {
    if ( root.joms_assets_url ) {
        load();
       
    } else {
        root.joms.warn( 'Variable `joms_assets_url` is not defined.' );
    }
});

})( this );

joms || (joms = {});
joms.map = {

    // callback queue
    queue: [],

    // google map proxy
    execute: function( callback ) { 
        
        if(this.type == "openstreetmap"){
            this.executeOpenStreetmap(callback);
        }else{
            this.executeGoogle(callback);
        }
      
    },
    
    executeGoogle: function(callback){
        if ( window.google && window.google.maps && window.google.maps.places ) {
            callback();
            return;
        }

        if ( joms.map.loading ) {
            joms.map.queue.push( callback );
            return;
        }

        joms.map.loading = true;
        joms.map.queue.push( callback );
        joms.map.loadScript();
    },
    
    executeOpenStreetmap: function(callback){
        if ( window.L && window.L.map) {
            callback();
            return;
        }

        if ( joms.map.loading ) {
            joms.map.queue.push( callback );
            return;
        }

        joms.map.loading = true;
        joms.map.queue.push( callback );
        joms.map.loadScriptOpenstreet();
    },

    // google map library loader
    loadScript: function() { 
        if(this.type == "openstreetmap"){
            this.executeOpenStreetmap();
        }else{
            this.loadScriptGoogle();
        }
    },

    loadScriptGoogle: function(){

        var script = document.createElement('script');
        script.type = 'text/javascript';
        script.src = '//maps.googleapis.com/maps/api/js?libraries=places&sensor=false&callback=joms.map.loadScriptCallback';
        document.body.appendChild(script);

    },

    loadScriptOpenstreet: function(){
        var r ;
        r = false;
        var script = document.createElement("script");
        script.type = "text/javascript";
        script.src = "https://unpkg.com/leaflet@1.3.4/dist/leaflet.js";

        document.body.appendChild(script);
        
        script.onload = script.onreadystatechange = function() {
            
            if (!r && (!this.readyState || this.readyState == 'complete')) {
                 r = true;
                joms.map.loadScriptCallback();
            }
        };

        //script = document.createElement("script");
        //script.type = "text/javascript";
        //script.src = "https://unpkg.com/leaflet.markercluster@1.4.1/dist/leaflet.markercluster-src.js";

       //document.body.appendChild(script);
        var script2 = document.createElement("script");
        if(typeof openstreetmap == "undefined"){
                script2 = document.createElement( 'script' );
                script2.type = 'text/javascript';
                script2.src = joms.ASSETS_URL+'source/js/utils/openstreet.js';
            
                document.body.appendChild( script2 );
        }
        jQuery("<link>")
                .appendTo("head")
                .attr({
                    type: "text/css",
                    rel: "stylesheet",
                            href: "https://unpkg.com/leaflet@1.3.4/dist/leaflet.css"
                });
         jQuery("<link>")
                .appendTo("head")
                .attr({
                    type: "text/css",
                    rel: "stylesheet",
                            href: "https://unpkg.com/leaflet.markercluster@1.4.1/dist/MarkerCluster.css"
                });
         jQuery("<link>")
                .appendTo("head")
                .attr({
                    type: "text/css",
                    rel: "stylesheet",
                            href: "https://unpkg.com/leaflet.markercluster@1.4.1/dist/MarkerCluster.Default.css"
                }); 
        

    },

    // callback for google map library loader
    loadScriptCallback: function() {
        if ( joms.map.queue && joms.map.queue.length )
            while ( joms.map.queue.length )
                ( joms.map.queue.shift() )();

        joms.map.loading = false;
    }

};

