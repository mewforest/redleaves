(function( factory ) {

    var JomsObserver = factory();

    /**
     * JomsObserver global instance.
     * @name joms_observer
     * @type {JomsObserver}
     */
    joms_observer = new JomsObserver;

})(function() {

/**
 * JomsObserver class.
 * @class JomsObserver
 */
function JomsObserver() {}

/**
 * Filter and action list.
 * @memberof JomsObserver
 * @type {object}
 */
JomsObserver.prototype._filters = undefined;

/**
 * Filter callback identifier counter.
 * @memberof JomsObserver
 * @type {number}
 */
JomsObserver.prototype._guid = 1;

/**
 * Add filter hook to allow peepso extensions to modify various types of internal data at runtime.
 * @memberof JomsObserver
 * @param {string} name The name of the filter to hook the <code>fn</code> callback to.
 * @param {function} fn The callback to be run when the filter is applied.
 * @param {number} [priority=10] Used to specify the order in which the functions associated with a particular action are executed.
 * Lower numbers correspond with earlier execution, and functions with the same priority are executed
 * in the order in which they were added to the action.
 * @param {number} [num_param=0] The number of parameters the function accepts.
 * @param {object} [context] The context in which the <code>fn</code> callback will be called.
 */
JomsObserver.prototype.add_filter = function( name, fn, priority, num_param, context ) {
    var guid, filter;

    if ( typeof fn !== 'function' ) {
        return;
    }

    priority = priority || 10;

    guid = fn.joms_observer_id = fn.joms_observer_id || this._guid++;

    filter = {
        fn: fn,
        priority: priority,
        num_param: num_param,
        context: context
    };

    if ( !this._filters ) {
        this._filters = {};
    }

    if ( !this._filters[ name ] ) {
        this._filters[ name ] = {};
    }

    if ( !this._filters[ name ][ priority ] ) {
        this._filters[ name ][ priority ] = {};
    }

    this._filters[ name ][ priority ][ guid ] = filter;
};

/**
 * Remove filter hook previously added via <code>add_filter</code> method.
 * @memberof JomsObserver
 * @param {string} name The action hook to which the function to be removed is hooked.
 * @param {function} fn The callback for the function which should be removed.
 * @param {number} [priority=10] The priority of the function (as defined when the function was originally hooked).
 */
JomsObserver.prototype.remove_filter = function( name, fn, priority ) {
    var guid;

    if ( typeof fn !== 'function' ) {
        return;
    }

    priority = priority || 10;

    guid = fn.joms_observer_id;

    if ( guid && this._filters && this._filters[ name ] && this._filters[ name ][ priority ] && this._filters[ name ][ priority ][ guid ] ) {
        delete this._filters[ name ][ priority ][ guid ];
    }
};

/**
 * Call the functions added to a filter hook.
 * @memberof JomsObserver
 * @param {string} name The action hook to which the function to be removed is hooked.
 * @param {mixed} value The value on which the filters hooked to <code>name</code> are applied on.
 * @param {...mixed} [var] Additional variables passed to the functions hooked to <code>name</code>.
 * @return {mixed} The filtered value after all hooked functions are applied to it.
 */
JomsObserver.prototype.apply_filters = function( name ) {
    var args = arguments,
        data = '',
        filters = this._filters && this._filters[ name ],
        priority, guid, filter, fn_args, index;

    if ( !filters ) {
        return args[1];
    }

    for ( priority in filters ) {
        for ( guid in filters[ priority ] ) {
            filter = filters[ priority ][ guid ];
            if ( filter.num_param ) {
                fn_args = [];
                index = 1;
                while ( index <= filter.num_param ) {
                    fn_args.push( args[ index ] );
                    index++;
                }
                try {
                    data = filter.fn.apply( filter.context, fn_args );
                    args[1] = data;
                } catch ( e ) {}
            } else {
                try {
                    data = filter.fn();
                } catch ( e ) {}
            }
        }
    }

    return data;
};

/**
 * Add action hook to allow peepso extensions to listen when specific events occur at runtime.
 * @memberof JomsObserver
 * @param {string} name The name of the action to hook the <code>fn</code> callback to.
 * @param {function} fn The callback to be run when the action is applied.
 * @param {number} [priority=10] Used to specify the order in which the functions associated with a particular action are executed.
 * Lower numbers correspond with earlier execution, and functions with the same priority are executed
 * in the order in which they were added to the action.
 * @param {number} [num_param=0] The number of parameters the function accepts.
 * @param {object} [context] The context in which the <code>fn</code> callback will be called.
 */
JomsObserver.prototype.add_action = function( name, fn, priority, num_param, context ) {
    this.add_filter( name, fn, priority, num_param, context );
};

/**
 * Remove action hook previously added via <code>add_action</code> method.
 * @memberof JomsObserver
 * @param {string} name The action hook to which the function to be removed is hooked.
 * @param {function} fn The callback for the function which should be removed.
 * @param {number} [priority=10] The priority of the function (as defined when the function was originally hooked).
 */
JomsObserver.prototype.remove_action = function( name, fn, priority ) {
    this.remove_filter( name, fn, priority );
};

/**
 * Call the functions added to a action hook.
 * @memberof JomsObserver
 * @param {string} name The action hook to which the function to be removed is hooked.
 * @param {mixed} value The value on which the actions hooked to <code>name</code> are applied on.
 * @param {...mixed} [var] Additional variables passed to the functions hooked to <code>name</code>.
 */
JomsObserver.prototype.do_action = function( name ) {
    var args = arguments,
        actions = this._filters && this._filters[ name ],
        priority, guid, action, fn_args, index;

    if ( !actions ) {
        return;
    }

    for ( priority in actions ) {
        for ( guid in actions[ priority ] ) {
            action = actions[ priority ][ guid ];
            fn_args = [];
            if ( action.num_param ) {
                index = 1;
                while ( index <= action.num_param ) {
                    fn_args.push( args[ index ] );
                    index++;
                }
            }
            try {
                action.fn.apply( action.context, fn_args );
            } catch ( e ) {}
        }
    }
};

return JomsObserver;

});
