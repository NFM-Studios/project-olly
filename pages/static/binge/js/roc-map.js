!function ($) {
    "use strict";
    $(function () {
        $.support.transition = function () {
            var transitionEnd = function () {
                var name, el = document.createElement("bootstrap"), transEndEventNames = {
                    WebkitTransition: "webkitTransitionEnd",
                    MozTransition: "transitionend",
                    OTransition: "oTransitionEnd otransitionend",
                    transition: "transitionend"
                };
                for (name in transEndEventNames) if (void 0 !== el.style[name]) return transEndEventNames[name]
            }();
            return transitionEnd && {end: transitionEnd}
        }()
    })
}(window.jQuery), !function ($) {
    "use strict";
    var dismiss = '[data-dismiss="alert"]', Alert = function (el) {
        $(el).on("click", dismiss, this.close)
    };
    Alert.prototype.close = function (e) {
        function removeElement() {
            $parent.trigger("closed").remove()
        }

        var $parent, $this = $(this), selector = $this.attr("data-target");
        selector || (selector = $this.attr("href"), selector = selector && selector.replace(/.*(?=#[^\s]*$)/, "")), $parent = $(selector), e && e.preventDefault(), $parent.length || ($parent = $this.hasClass("alert") ? $this : $this.parent()), $parent.trigger(e = $.Event("close")), e.isDefaultPrevented() || ($parent.removeClass("in"), $.support.transition && $parent.hasClass("fade") ? $parent.on($.support.transition.end, removeElement) : removeElement())
    };
    var old = $.fn.alert;
    $.fn.alert = function (option) {
        return this.each(function () {
            var $this = $(this), data = $this.data("alert");
            data || $this.data("alert", data = new Alert(this)), "string" == typeof option && data[option].call($this)
        })
    }, $.fn.alert.Constructor = Alert, $.fn.alert.noConflict = function () {
        return $.fn.alert = old, this
    }, $(document).on("click.alert.data-api", dismiss, Alert.prototype.close)
}(window.jQuery), !function ($) {
    "use strict";
    var Button = function (element, options) {
        this.$element = $(element), this.options = $.extend({}, $.fn.button.defaults, options)
    };
    Button.prototype.setState = function (state) {
        var d = "disabled", $el = this.$element, data = $el.data(), val = $el.is("input") ? "val" : "html";
        state += "Text", data.resetText || $el.data("resetText", $el[val]()), $el[val](data[state] || this.options[state]), setTimeout(function () {
            "loadingText" == state ? $el.addClass(d).attr(d, d) : $el.removeClass(d).removeAttr(d)
        }, 0)
    }, Button.prototype.toggle = function () {
        var $parent = this.$element.closest('[data-toggle="buttons-radio"]');
        $parent && $parent.find(".active").removeClass("active"), this.$element.toggleClass("active")
    };
    var old = $.fn.button;
    $.fn.button = function (option) {
        return this.each(function () {
            var $this = $(this), data = $this.data("button"), options = "object" == typeof option && option;
            data || $this.data("button", data = new Button(this, options)), "toggle" == option ? data.toggle() : option && data.setState(option)
        })
    }, $.fn.button.defaults = {loadingText: "loading..."}, $.fn.button.Constructor = Button, $.fn.button.noConflict = function () {
        return $.fn.button = old, this
    }, $(document).on("click.button.data-api", "[data-toggle^=button]", function (e) {
        var $btn = $(e.target);
        $btn.hasClass("btn") || ($btn = $btn.closest(".btn")), $btn.button("toggle")
    })
}(window.jQuery), !function ($) {
    "use strict";
    var Carousel = function (element, options) {
        this.$element = $(element), this.options = options, "hover" == this.options.pause && this.$element.on("mouseenter", $.proxy(this.pause, this)).on("mouseleave", $.proxy(this.cycle, this))
    };
    Carousel.prototype = {
        cycle: function (e) {
            return e || (this.paused = !1), this.options.interval && !this.paused && (this.interval = setInterval($.proxy(this.next, this), this.options.interval)), this
        }, to: function (pos) {
            var $active = this.$element.find(".item.active"), children = $active.parent().children(),
                activePos = children.index($active), that = this;
            if (!(pos > children.length - 1 || 0 > pos)) return this.sliding ? this.$element.one("slid", function () {
                that.to(pos)
            }) : activePos == pos ? this.pause().cycle() : this.slide(pos > activePos ? "next" : "prev", $(children[pos]))
        }, pause: function (e) {
            return e || (this.paused = !0), this.$element.find(".next, .prev").length && $.support.transition.end && (this.$element.trigger($.support.transition.end), this.cycle()), clearInterval(this.interval), this.interval = null, this
        }, next: function () {
            return this.sliding ? void 0 : this.slide("next")
        }, prev: function () {
            return this.sliding ? void 0 : this.slide("prev")
        }, slide: function (type, next) {
            var e, $active = this.$element.find(".item.active"), $next = next || $active[type](),
                isCycling = this.interval, direction = "next" == type ? "left" : "right",
                fallback = "next" == type ? "first" : "last", that = this;
            if (this.sliding = !0, isCycling && this.pause(), $next = $next.length ? $next : this.$element.find(".item")[fallback](), e = $.Event("slide", {relatedTarget: $next[0]}), !$next.hasClass("active")) {
                if ($.support.transition && this.$element.hasClass("slide")) {
                    if (this.$element.trigger(e), e.isDefaultPrevented()) return;
                    $next.addClass(type), $next[0].offsetWidth, $active.addClass(direction), $next.addClass(direction), this.$element.one($.support.transition.end, function () {
                        $next.removeClass([type, direction].join(" ")).addClass("active"), $active.removeClass(["active", direction].join(" ")), that.sliding = !1, setTimeout(function () {
                            that.$element.trigger("slid")
                        }, 0)
                    })
                } else {
                    if (this.$element.trigger(e), e.isDefaultPrevented()) return;
                    $active.removeClass("active"), $next.addClass("active"), this.sliding = !1, this.$element.trigger("slid")
                }
                return isCycling && this.cycle(), this
            }
        }
    };
    var old = $.fn.carousel;
    $.fn.carousel = function (option) {
        return this.each(function () {
            var $this = $(this), data = $this.data("carousel"),
                options = $.extend({}, $.fn.carousel.defaults, "object" == typeof option && option),
                action = "string" == typeof option ? option : options.slide;
            data || $this.data("carousel", data = new Carousel(this, options)), "number" == typeof option ? data.to(option) : action ? data[action]() : options.interval && data.cycle()
        })
    }, $.fn.carousel.defaults = {
        interval: 5e3,
        pause: "hover"
    }, $.fn.carousel.Constructor = Carousel, $.fn.carousel.noConflict = function () {
        return $.fn.carousel = old, this
    }, $(document).on("click.carousel.data-api", "[data-slide]", function (e) {
        var href, $this = $(this),
            $target = $($this.attr("data-target") || (href = $this.attr("href")) && href.replace(/.*(?=#[^\s]+$)/, "")),
            options = $.extend({}, $target.data(), $this.data());
        $target.carousel(options), e.preventDefault()
    })
}(window.jQuery), !function ($) {
    "use strict";
    var Collapse = function (element, options) {
        this.$element = $(element), this.options = $.extend({}, $.fn.collapse.defaults, options), this.options.parent && (this.$parent = $(this.options.parent)), this.options.toggle && this.toggle()
    };
    Collapse.prototype = {
        constructor: Collapse, dimension: function () {
            var hasWidth = this.$element.hasClass("width");
            return hasWidth ? "width" : "height"
        }, show: function () {
            var dimension, scroll, actives, hasData;
            if (!this.transitioning) {
                if (dimension = this.dimension(), scroll = $.camelCase(["scroll", dimension].join("-")), actives = this.$parent && this.$parent.find("> .accordion-group > .in"), actives && actives.length) {
                    if (hasData = actives.data("collapse"), hasData && hasData.transitioning) return;
                    actives.collapse("hide"), hasData || actives.data("collapse", null)
                }
                this.$element[dimension](0), this.transition("addClass", $.Event("show"), "shown"), $.support.transition && this.$element[dimension](this.$element[0][scroll])
            }
        }, hide: function () {
            var dimension;
            this.transitioning || (dimension = this.dimension(), this.reset(this.$element[dimension]()), this.transition("removeClass", $.Event("hide"), "hidden"), this.$element[dimension](0))
        }, reset: function (size) {
            var dimension = this.dimension();
            return this.$element.removeClass("collapse")[dimension](size || "auto")[0].offsetWidth, this.$element[null !== size ? "addClass" : "removeClass"]("collapse"), this
        }, transition: function (method, startEvent, completeEvent) {
            var that = this, complete = function () {
                "show" == startEvent.type && that.reset(), that.transitioning = 0, that.$element.trigger(completeEvent)
            };
            this.$element.trigger(startEvent), startEvent.isDefaultPrevented() || (this.transitioning = 1, this.$element[method]("in"), $.support.transition && this.$element.hasClass("collapse") ? this.$element.one($.support.transition.end, complete) : complete())
        }, toggle: function () {
            this[this.$element.hasClass("in") ? "hide" : "show"]()
        }
    };
    var old = $.fn.collapse;
    $.fn.collapse = function (option) {
        return this.each(function () {
            var $this = $(this), data = $this.data("collapse"), options = "object" == typeof option && option;
            data || $this.data("collapse", data = new Collapse(this, options)), "string" == typeof option && data[option]()
        })
    }, $.fn.collapse.defaults = {toggle: !0}, $.fn.collapse.Constructor = Collapse, $.fn.collapse.noConflict = function () {
        return $.fn.collapse = old, this
    }, $(document).on("click.collapse.data-api", "[data-toggle=collapse]", function (e) {
        var href, $this = $(this),
            target = $this.attr("data-target") || e.preventDefault() || (href = $this.attr("href")) && href.replace(/.*(?=#[^\s]+$)/, ""),
            option = $(target).data("collapse") ? "toggle" : $this.data();
        $this[$(target).hasClass("in") ? "addClass" : "removeClass"]("collapsed"), $(target).collapse(option)
    })
}(window.jQuery), !function ($) {
    "use strict";

    function clearMenus() {
        $(toggle).each(function () {
            getParent($(this)).removeClass("open")
        })
    }

    function getParent($this) {
        var $parent, selector = $this.attr("data-target");
        return selector || (selector = $this.attr("href"), selector = selector && /#/.test(selector) && selector.replace(/.*(?=#[^\s]*$)/, "")), $parent = $(selector), $parent.length || ($parent = $this.parent()), $parent
    }

    var toggle = "[data-toggle=dropdown]", Dropdown = function (element) {
        var $el = $(element).on("click.dropdown.data-api", this.toggle);
        $("html").on("click.dropdown.data-api", function () {
            $el.parent().removeClass("open")
        })
    };
    Dropdown.prototype = {
        constructor: Dropdown, toggle: function () {
            var $parent, isActive, $this = $(this);
            if (!$this.is(".disabled, :disabled")) return $parent = getParent($this), isActive = $parent.hasClass("open"), clearMenus(), isActive || $parent.toggleClass("open"), $this.focus(), !1
        }, keydown: function (e) {
            var $this, $items, $parent, isActive, index;
            if (/(38|40|27)/.test(e.keyCode) && ($this = $(this), e.preventDefault(), e.stopPropagation(), !$this.is(".disabled, :disabled"))) {
                if ($parent = getParent($this), isActive = $parent.hasClass("open"), !isActive || isActive && 27 == e.keyCode) return $this.click();
                $items = $("[role=menu] li:not(.divider):visible a", $parent), $items.length && (index = $items.index($items.filter(":focus")), 38 == e.keyCode && index > 0 && index--, 40 == e.keyCode && $items.length - 1 > index && index++, ~index || (index = 0), $items.eq(index).focus())
            }
        }
    };
    var old = $.fn.dropdown;
    $.fn.dropdown = function (option) {
        return this.each(function () {
            var $this = $(this), data = $this.data("dropdown");
            data || $this.data("dropdown", data = new Dropdown(this)), "string" == typeof option && data[option].call($this)
        })
    }, $.fn.dropdown.Constructor = Dropdown, $.fn.dropdown.noConflict = function () {
        return $.fn.dropdown = old, this
    }, $(document).on("click.dropdown.data-api touchstart.dropdown.data-api", clearMenus).on("click.dropdown touchstart.dropdown.data-api", ".dropdown form", function (e) {
        e.stopPropagation()
    }).on("touchstart.dropdown.data-api", ".dropdown-menu", function (e) {
        e.stopPropagation()
    }).on("click.dropdown.data-api touchstart.dropdown.data-api", toggle, Dropdown.prototype.toggle).on("keydown.dropdown.data-api touchstart.dropdown.data-api", toggle + ", [role=menu]", Dropdown.prototype.keydown)
}(window.jQuery), !function ($) {
    "use strict";
    var Modal = function (element, options) {
        this.options = options, this.$element = $(element).delegate('[data-dismiss="modal"]', "click.dismiss.modal", $.proxy(this.hide, this)), this.options.remote && this.$element.find(".modal-body").load(this.options.remote)
    };
    Modal.prototype = {
        constructor: Modal, toggle: function () {
            return this[this.isShown ? "hide" : "show"]()
        }, show: function () {
            var that = this, e = $.Event("show");
            this.$element.trigger(e), this.isShown || e.isDefaultPrevented() || (this.isShown = !0, this.escape(), this.backdrop(function () {
                var transition = $.support.transition && that.$element.hasClass("fade");
                that.$element.parent().length || that.$element.appendTo(document.body), that.$element.show(), transition && that.$element[0].offsetWidth, that.$element.addClass("in").attr("aria-hidden", !1), that.enforceFocus(), transition ? that.$element.one($.support.transition.end, function () {
                    that.$element.focus().trigger("shown")
                }) : that.$element.focus().trigger("shown")
            }))
        }, hide: function (e) {
            e && e.preventDefault(), e = $.Event("hide"), this.$element.trigger(e), this.isShown && !e.isDefaultPrevented() && (this.isShown = !1, this.escape(), $(document).off("focusin.modal"), this.$element.removeClass("in").attr("aria-hidden", !0), $.support.transition && this.$element.hasClass("fade") ? this.hideWithTransition() : this.hideModal())
        }, enforceFocus: function () {
            var that = this;
            $(document).on("focusin.modal", function (e) {
                that.$element[0] === e.target || that.$element.has(e.target).length || that.$element.focus()
            })
        }, escape: function () {
            var that = this;
            this.isShown && this.options.keyboard ? this.$element.on("keyup.dismiss.modal", function (e) {
                27 == e.which && that.hide()
            }) : this.isShown || this.$element.off("keyup.dismiss.modal")
        }, hideWithTransition: function () {
            var that = this, timeout = setTimeout(function () {
                that.$element.off($.support.transition.end), that.hideModal()
            }, 500);
            this.$element.one($.support.transition.end, function () {
                clearTimeout(timeout), that.hideModal()
            })
        }, hideModal: function () {
            this.$element.hide().trigger("hidden"), this.backdrop()
        }, removeBackdrop: function () {
            this.$backdrop.remove(), this.$backdrop = null
        }, backdrop: function (callback) {
            var animate = this.$element.hasClass("fade") ? "fade" : "";
            if (this.isShown && this.options.backdrop) {
                var doAnimate = $.support.transition && animate;
                this.$backdrop = $('<div class="modal-backdrop ' + animate + '" />').appendTo(document.body), this.$backdrop.click("static" == this.options.backdrop ? $.proxy(this.$element[0].focus, this.$element[0]) : $.proxy(this.hide, this)), doAnimate && this.$backdrop[0].offsetWidth, this.$backdrop.addClass("in"), doAnimate ? this.$backdrop.one($.support.transition.end, callback) : callback()
            } else !this.isShown && this.$backdrop ? (this.$backdrop.removeClass("in"), $.support.transition && this.$element.hasClass("fade") ? this.$backdrop.one($.support.transition.end, $.proxy(this.removeBackdrop, this)) : this.removeBackdrop()) : callback && callback()
        }
    };
    var old = $.fn.modal;
    $.fn.modal = function (option) {
        return this.each(function () {
            var $this = $(this), data = $this.data("modal"),
                options = $.extend({}, $.fn.modal.defaults, $this.data(), "object" == typeof option && option);
            data || $this.data("modal", data = new Modal(this, options)), "string" == typeof option ? data[option]() : options.show && data.show()
        })
    }, $.fn.modal.defaults = {
        backdrop: !0,
        keyboard: !0,
        show: !0
    }, $.fn.modal.Constructor = Modal, $.fn.modal.noConflict = function () {
        return $.fn.modal = old, this
    }, $(document).on("click.modal.data-api", '[data-toggle="modal"]', function (e) {
        var $this = $(this), href = $this.attr("href"),
            $target = $($this.attr("data-target") || href && href.replace(/.*(?=#[^\s]+$)/, "")),
            option = $target.data("modal") ? "toggle" : $.extend({remote: !/#/.test(href) && href}, $target.data(), $this.data());
        e.preventDefault(), $target.modal(option).one("hide", function () {
            $this.focus()
        })
    })
}(window.jQuery), !function ($) {
    "use strict";
    var Tooltip = function (element, options) {
        this.init("tooltip", element, options)
    };
    Tooltip.prototype = {
        constructor: Tooltip, init: function (type, element, options) {
            var eventIn, eventOut;
            this.type = type, this.$element = $(element), this.options = this.getOptions(options), this.enabled = !0, "click" == this.options.trigger ? this.$element.on("click." + this.type, this.options.selector, $.proxy(this.toggle, this)) : "manual" != this.options.trigger && (eventIn = "hover" == this.options.trigger ? "mouseenter" : "focus", eventOut = "hover" == this.options.trigger ? "mouseleave" : "blur", this.$element.on(eventIn + "." + this.type, this.options.selector, $.proxy(this.enter, this)), this.$element.on(eventOut + "." + this.type, this.options.selector, $.proxy(this.leave, this))), this.options.selector ? this._options = $.extend({}, this.options, {
                trigger: "manual",
                selector: ""
            }) : this.fixTitle()
        }, getOptions: function (options) {
            return options = $.extend({}, $.fn[this.type].defaults, options, this.$element.data()), options.delay && "number" == typeof options.delay && (options.delay = {
                show: options.delay,
                hide: options.delay
            }), options
        }, enter: function (e) {
            var self = $(e.currentTarget)[this.type](this._options).data(this.type);
            return self.options.delay && self.options.delay.show ? (clearTimeout(this.timeout), self.hoverState = "in", this.timeout = setTimeout(function () {
                "in" == self.hoverState && self.show()
            }, self.options.delay.show), void 0) : self.show()
        }, leave: function (e) {
            var self = $(e.currentTarget)[this.type](this._options).data(this.type);
            return this.timeout && clearTimeout(this.timeout), self.options.delay && self.options.delay.hide ? (self.hoverState = "out", this.timeout = setTimeout(function () {
                "out" == self.hoverState && self.hide()
            }, self.options.delay.hide), void 0) : self.hide()
        }, show: function () {
            var $tip, inside, pos, actualWidth, actualHeight, placement, tp;
            if (this.hasContent() && this.enabled) {
                switch ($tip = this.tip(), this.setContent(), this.options.animation && $tip.addClass("fade"), placement = "function" == typeof this.options.placement ? this.options.placement.call(this, $tip[0], this.$element[0]) : this.options.placement, inside = /in/.test(placement), $tip.detach().css({
                    top: 0,
                    left: 0,
                    display: "block"
                }).insertAfter(this.$element), pos = this.getPosition(inside), actualWidth = $tip[0].offsetWidth, actualHeight = $tip[0].offsetHeight, inside ? placement.split(" ")[1] : placement) {
                    case "bottom":
                        tp = {top: pos.top + pos.height, left: pos.left + pos.width / 2 - actualWidth / 2};
                        break;
                    case "top":
                        tp = {top: pos.top - actualHeight, left: pos.left + pos.width / 2 - actualWidth / 2};
                        break;
                    case "left":
                        tp = {top: pos.top + pos.height / 2 - actualHeight / 2, left: pos.left - actualWidth};
                        break;
                    case "right":
                        tp = {top: pos.top + pos.height / 2 - actualHeight / 2, left: pos.left + pos.width}
                }
                $tip.offset(tp).addClass(placement).addClass("in")
            }
        }, setContent: function () {
            var $tip = this.tip(), title = this.getTitle();
            $tip.find(".tooltip-inner")[this.options.html ? "html" : "text"](title), $tip.removeClass("fade in top bottom left right")
        }, hide: function () {
            function removeWithAnimation() {
                var timeout = setTimeout(function () {
                    $tip.off($.support.transition.end).detach()
                }, 500);
                $tip.one($.support.transition.end, function () {
                    clearTimeout(timeout), $tip.detach()
                })
            }

            var $tip = this.tip();
            return $tip.removeClass("in"), $.support.transition && this.$tip.hasClass("fade") ? removeWithAnimation() : $tip.detach(), this
        }, fixTitle: function () {
            var $e = this.$element;
            ($e.attr("title") || "string" != typeof $e.attr("data-original-title")) && $e.attr("data-original-title", $e.attr("title") || "").removeAttr("title")
        }, hasContent: function () {
            return this.getTitle()
        }, getPosition: function (inside) {
            return $.extend({}, inside ? {
                top: 0,
                left: 0
            } : this.$element.offset(), {width: this.$element[0].offsetWidth, height: this.$element[0].offsetHeight})
        }, getTitle: function () {
            var title, $e = this.$element, o = this.options;
            return title = $e.attr("data-original-title") || ("function" == typeof o.title ? o.title.call($e[0]) : o.title)
        }, tip: function () {
            return this.$tip = this.$tip || $(this.options.template)
        }, validate: function () {
            this.$element[0].parentNode || (this.hide(), this.$element = null, this.options = null)
        }, enable: function () {
            this.enabled = !0
        }, disable: function () {
            this.enabled = !1
        }, toggleEnabled: function () {
            this.enabled = !this.enabled
        }, toggle: function (e) {
            var self = $(e.currentTarget)[this.type](this._options).data(this.type);
            self[self.tip().hasClass("in") ? "hide" : "show"]()
        }, destroy: function () {
            this.hide().$element.off("." + this.type).removeData(this.type)
        }
    };
    var old = $.fn.tooltip;
    $.fn.tooltip = function (option) {
        return this.each(function () {
            var $this = $(this), data = $this.data("tooltip"), options = "object" == typeof option && option;
            data || $this.data("tooltip", data = new Tooltip(this, options)), "string" == typeof option && data[option]()
        })
    }, $.fn.tooltip.Constructor = Tooltip, $.fn.tooltip.defaults = {
        animation: !0,
        placement: "top",
        selector: !1,
        template: '<div class="tooltip"><div class="tooltip-arrow"></div><div class="tooltip-inner"></div></div>',
        trigger: "hover",
        title: "",
        delay: 0,
        html: !1
    }, $.fn.tooltip.noConflict = function () {
        return $.fn.tooltip = old, this
    }
}(window.jQuery), !function ($) {
    "use strict";
    var Popover = function (element, options) {
        this.init("popover", element, options)
    };
    Popover.prototype = $.extend({}, $.fn.tooltip.Constructor.prototype, {
        constructor: Popover,
        setContent: function () {
            var $tip = this.tip(), title = this.getTitle(), content = this.getContent();
            $tip.find(".popover-title")[this.options.html ? "html" : "text"](title), $tip.find(".popover-content")[this.options.html ? "html" : "text"](content), $tip.removeClass("fade top bottom left right in")
        },
        hasContent: function () {
            return this.getTitle() || this.getContent()
        },
        getContent: function () {
            var content, $e = this.$element, o = this.options;
            return content = $e.attr("data-content") || ("function" == typeof o.content ? o.content.call($e[0]) : o.content)
        },
        tip: function () {
            return this.$tip || (this.$tip = $(this.options.template)), this.$tip
        },
        destroy: function () {
            this.hide().$element.off("." + this.type).removeData(this.type)
        }
    });
    var old = $.fn.popover;
    $.fn.popover = function (option) {
        return this.each(function () {
            var $this = $(this), data = $this.data("popover"), options = "object" == typeof option && option;
            data || $this.data("popover", data = new Popover(this, options)), "string" == typeof option && data[option]()
        })
    }, $.fn.popover.Constructor = Popover, $.fn.popover.defaults = $.extend({}, $.fn.tooltip.defaults, {
        placement: "right",
        trigger: "click",
        content: "",
        template: '<div class="popover"><div class="arrow"></div><div class="popover-inner"><h3 class="popover-title"></h3><div class="popover-content"></div></div></div>'
    }), $.fn.popover.noConflict = function () {
        return $.fn.popover = old, this
    }
}(window.jQuery), !function ($) {
    "use strict";

    function ScrollSpy(element, options) {
        var href, process = $.proxy(this.process, this), $element = $(element).is("body") ? $(window) : $(element);
        this.options = $.extend({}, $.fn.scrollspy.defaults, options), this.$scrollElement = $element.on("scroll.scroll-spy.data-api", process), this.selector = (this.options.target || (href = $(element).attr("href")) && href.replace(/.*(?=#[^\s]+$)/, "") || "") + " .nav li > a", this.$body = $("body"), this.refresh(), this.process()
    }

    ScrollSpy.prototype = {
        constructor: ScrollSpy, refresh: function () {
            var $targets, self = this;
            this.offsets = $([]), this.targets = $([]), $targets = this.$body.find(this.selector).map(function () {
                var $el = $(this), href = $el.data("target") || $el.attr("href"), $href = /^#\w/.test(href) && $(href);
                return $href && $href.length && [[$href.position().top + self.$scrollElement.scrollTop(), href]] || null
            }).sort(function (a, b) {
                return a[0] - b[0]
            }).each(function () {
                self.offsets.push(this[0]), self.targets.push(this[1])
            })
        }, process: function () {
            var i, scrollTop = this.$scrollElement.scrollTop() + this.options.offset,
                scrollHeight = this.$scrollElement[0].scrollHeight || this.$body[0].scrollHeight,
                maxScroll = scrollHeight - this.$scrollElement.height(), offsets = this.offsets, targets = this.targets,
                activeTarget = this.activeTarget;
            if (scrollTop >= maxScroll) return activeTarget != (i = targets.last()[0]) && this.activate(i);
            for (i = offsets.length; i--;) activeTarget != targets[i] && scrollTop >= offsets[i] && (!offsets[i + 1] || offsets[i + 1] >= scrollTop) && this.activate(targets[i])
        }, activate: function (target) {
            var active, selector;
            this.activeTarget = target, $(this.selector).parent(".active").removeClass("active"), selector = this.selector + '[data-target="' + target + '"],' + this.selector + '[href="' + target + '"]', active = $(selector).parent("li").addClass("active"), active.parent(".dropdown-menu").length && (active = active.closest("li.dropdown").addClass("active")), active.trigger("activate")
        }
    };
    var old = $.fn.scrollspy;
    $.fn.scrollspy = function (option) {
        return this.each(function () {
            var $this = $(this), data = $this.data("scrollspy"), options = "object" == typeof option && option;
            data || $this.data("scrollspy", data = new ScrollSpy(this, options)), "string" == typeof option && data[option]()
        })
    }, $.fn.scrollspy.Constructor = ScrollSpy, $.fn.scrollspy.defaults = {offset: 10}, $.fn.scrollspy.noConflict = function () {
        return $.fn.scrollspy = old, this
    }, $(window).on("load", function () {
        $('[data-spy="scroll"]').each(function () {
            var $spy = $(this);
            $spy.scrollspy($spy.data())
        })
    })
}(window.jQuery), !function ($) {
    "use strict";
    var Tab = function (element) {
        this.element = $(element)
    };
    Tab.prototype = {
        constructor: Tab, show: function () {
            var previous, $target, e, $this = this.element, $ul = $this.closest("ul:not(.dropdown-menu)"),
                selector = $this.attr("data-target");
            selector || (selector = $this.attr("href"), selector = selector && selector.replace(/.*(?=#[^\s]*$)/, "")), $this.parent("li").hasClass("active") || (previous = $ul.find(".active:last a")[0], e = $.Event("show", {relatedTarget: previous}), $this.trigger(e), e.isDefaultPrevented() || ($target = $(selector), this.activate($this.parent("li"), $ul), this.activate($target, $target.parent(), function () {
                $this.trigger({type: "shown", relatedTarget: previous})
            })))
        }, activate: function (element, container, callback) {
            function next() {
                $active.removeClass("active").find("> .dropdown-menu > .active").removeClass("active"), element.addClass("active"), transition ? (element[0].offsetWidth, element.addClass("in")) : element.removeClass("fade"), element.parent(".dropdown-menu") && element.closest("li.dropdown").addClass("active"), callback && callback()
            }

            var $active = container.find("> .active"),
                transition = callback && $.support.transition && $active.hasClass("fade");
            transition ? $active.one($.support.transition.end, next) : next(), $active.removeClass("in")
        }
    };
    var old = $.fn.tab;
    $.fn.tab = function (option) {
        return this.each(function () {
            var $this = $(this), data = $this.data("tab");
            data || $this.data("tab", data = new Tab(this)), "string" == typeof option && data[option]()
        })
    }, $.fn.tab.Constructor = Tab, $.fn.tab.noConflict = function () {
        return $.fn.tab = old, this
    }, $(document).on("click.tab.data-api", '[data-toggle="tab"], [data-toggle="pill"]', function (e) {
        e.preventDefault(), $(this).tab("show")
    })
}(window.jQuery), !function ($) {
    "use strict";
    var Typeahead = function (element, options) {
        this.$element = $(element), this.options = $.extend({}, $.fn.typeahead.defaults, options), this.matcher = this.options.matcher || this.matcher, this.sorter = this.options.sorter || this.sorter, this.highlighter = this.options.highlighter || this.highlighter, this.updater = this.options.updater || this.updater, this.source = this.options.source, this.$menu = $(this.options.menu), this.shown = !1, this.listen()
    };
    Typeahead.prototype = {
        constructor: Typeahead, select: function () {
            var val = this.$menu.find(".active").attr("data-value");
            return this.$element.val(this.updater(val)).change(), this.hide()
        }, updater: function (item) {
            return item
        }, show: function () {
            var pos = $.extend({}, this.$element.position(), {height: this.$element[0].offsetHeight});
            return this.$menu.insertAfter(this.$element).css({
                top: pos.top + pos.height,
                left: pos.left
            }).show(), this.shown = !0, this
        }, hide: function () {
            return this.$menu.hide(), this.shown = !1, this
        }, lookup: function () {
            var items;
            return this.query = this.$element.val(), !this.query || this.query.length < this.options.minLength ? this.shown ? this.hide() : this : (items = $.isFunction(this.source) ? this.source(this.query, $.proxy(this.process, this)) : this.source, items ? this.process(items) : this)
        }, process: function (items) {
            var that = this;
            return items = $.grep(items, function (item) {
                return that.matcher(item)
            }), items = this.sorter(items), items.length ? this.render(items.slice(0, this.options.items)).show() : this.shown ? this.hide() : this
        }, matcher: function (item) {
            return ~item.toLowerCase().indexOf(this.query.toLowerCase())
        }, sorter: function (items) {
            for (var item, beginswith = [], caseSensitive = [], caseInsensitive = []; item = items.shift();) item.toLowerCase().indexOf(this.query.toLowerCase()) ? ~item.indexOf(this.query) ? caseSensitive.push(item) : caseInsensitive.push(item) : beginswith.push(item);
            return beginswith.concat(caseSensitive, caseInsensitive)
        }, highlighter: function (item) {
            var query = this.query.replace(/[\-\[\]{}()*+?.,\\\^$|#\s]/g, "\\$&");
            return item.replace(RegExp("(" + query + ")", "ig"), function ($1, match) {
                return "<strong>" + match + "</strong>"
            })
        }, render: function (items) {
            var that = this;
            return items = $(items).map(function (i, item) {
                return i = $(that.options.item).attr("data-value", item), i.find("a").html(that.highlighter(item)), i[0]
            }), items.first().addClass("active"), this.$menu.html(items), this
        }, next: function () {
            var active = this.$menu.find(".active").removeClass("active"), next = active.next();
            next.length || (next = $(this.$menu.find("li")[0])), next.addClass("active")
        }, prev: function () {
            var active = this.$menu.find(".active").removeClass("active"), prev = active.prev();
            prev.length || (prev = this.$menu.find("li").last()), prev.addClass("active")
        }, listen: function () {
            this.$element.on("blur", $.proxy(this.blur, this)).on("keypress", $.proxy(this.keypress, this)).on("keyup", $.proxy(this.keyup, this)), this.eventSupported("keydown") && this.$element.on("keydown", $.proxy(this.keydown, this)), this.$menu.on("click", $.proxy(this.click, this)).on("mouseenter", "li", $.proxy(this.mouseenter, this))
        }, eventSupported: function (eventName) {
            var isSupported = eventName in this.$element;
            return isSupported || (this.$element.setAttribute(eventName, "return;"), isSupported = "function" == typeof this.$element[eventName]), isSupported
        }, move: function (e) {
            if (this.shown) {
                switch (e.keyCode) {
                    case 9:
                    case 13:
                    case 27:
                        e.preventDefault();
                        break;
                    case 38:
                        e.preventDefault(), this.prev();
                        break;
                    case 40:
                        e.preventDefault(), this.next()
                }
                e.stopPropagation()
            }
        }, keydown: function (e) {
            this.suppressKeyPressRepeat = ~$.inArray(e.keyCode, [40, 38, 9, 13, 27]), this.move(e)
        }, keypress: function (e) {
            this.suppressKeyPressRepeat || this.move(e)
        }, keyup: function (e) {
            switch (e.keyCode) {
                case 40:
                case 38:
                case 16:
                case 17:
                case 18:
                    break;
                case 9:
                case 13:
                    if (!this.shown) return;
                    this.select();
                    break;
                case 27:
                    if (!this.shown) return;
                    this.hide();
                    break;
                default:
                    this.lookup()
            }
            e.stopPropagation(), e.preventDefault()
        }, blur: function () {
            var that = this;
            setTimeout(function () {
                that.hide()
            }, 150)
        }, click: function (e) {
            e.stopPropagation(), e.preventDefault(), this.select()
        }, mouseenter: function (e) {
            this.$menu.find(".active").removeClass("active"), $(e.currentTarget).addClass("active")
        }
    };
    var old = $.fn.typeahead;
    $.fn.typeahead = function (option) {
        return this.each(function () {
            var $this = $(this), data = $this.data("typeahead"), options = "object" == typeof option && option;
            data || $this.data("typeahead", data = new Typeahead(this, options)), "string" == typeof option && data[option]()
        })
    }, $.fn.typeahead.defaults = {
        source: [],
        items: 8,
        menu: '<ul class="typeahead dropdown-menu"></ul>',
        item: '<li><a href="#"></a></li>',
        minLength: 1
    }, $.fn.typeahead.Constructor = Typeahead, $.fn.typeahead.noConflict = function () {
        return $.fn.typeahead = old, this
    }, $(document).on("focus.typeahead.data-api", '[data-provide="typeahead"]', function (e) {
        var $this = $(this);
        $this.data("typeahead") || (e.preventDefault(), $this.typeahead($this.data()))
    })
}(window.jQuery), !function ($) {
    "use strict";
    var Affix = function (element, options) {
        this.options = $.extend({}, $.fn.affix.defaults, options), this.$window = $(window).on("scroll.affix.data-api", $.proxy(this.checkPosition, this)).on("click.affix.data-api", $.proxy(function () {
            setTimeout($.proxy(this.checkPosition, this), 1)
        }, this)), this.$element = $(element), this.checkPosition()
    };
    Affix.prototype.checkPosition = function () {
        if (this.$element.is(":visible")) {
            var affix, scrollHeight = $(document).height(), scrollTop = this.$window.scrollTop(),
                position = this.$element.offset(), offset = this.options.offset, offsetBottom = offset.bottom,
                offsetTop = offset.top, reset = "affix affix-top affix-bottom";
            "object" != typeof offset && (offsetBottom = offsetTop = offset), "function" == typeof offsetTop && (offsetTop = offset.top()), "function" == typeof offsetBottom && (offsetBottom = offset.bottom()), affix = null != this.unpin && scrollTop + this.unpin <= position.top ? !1 : null != offsetBottom && position.top + this.$element.height() >= scrollHeight - offsetBottom ? "bottom" : null != offsetTop && offsetTop >= scrollTop ? "top" : !1, this.affixed !== affix && (this.affixed = affix, this.unpin = "bottom" == affix ? position.top - scrollTop : null, this.$element.removeClass(reset).addClass("affix" + (affix ? "-" + affix : "")))
        }
    };
    var old = $.fn.affix;
    $.fn.affix = function (option) {
        return this.each(function () {
            var $this = $(this), data = $this.data("affix"), options = "object" == typeof option && option;
            data || $this.data("affix", data = new Affix(this, options)), "string" == typeof option && data[option]()
        })
    }, $.fn.affix.Constructor = Affix, $.fn.affix.defaults = {offset: 0}, $.fn.affix.noConflict = function () {
        return $.fn.affix = old, this
    }, $(window).on("load", function () {
        $('[data-spy="affix"]').each(function () {
            var $spy = $(this), data = $spy.data();
            data.offset = data.offset || {}, data.offsetBottom && (data.offset.bottom = data.offsetBottom), data.offsetTop && (data.offset.top = data.offsetTop), $spy.affix(data)
        })
    })
}(window.jQuery);
(function (a) {
    a.fn.LiteTooltip = function (d, c) {
        return this.each(function () {
            var f = a.extend({}, a.fn.LiteTooltip.defaultSettings, d || {});
            var e = a(this);
            var g = new b(f, e);
            if (g.settings.title != "") {
                if (!e.is("input")) {
                    e.css({cursor: "pointer"})
                }
                if (g.settings.trigger == "hoverable") {
                    this.toggle = false;
                    e.bind("mouseenter", {
                        settings: g.settings,
                        element: e,
                        $plugin: g,
                        $toggle: this.toggle
                    }, g.mouseOverHandler);
                    e.bind("mouseleave", {
                        settings: g.settings,
                        element: e,
                        $plugin: g,
                        $toggle: this.toggle
                    }, g.mouseOutHandler)
                } else {
                    if (g.settings.trigger == "hover") {
                        e.bind("mouseenter", {settings: g.settings, element: e, $plugin: g}, g.mouseOverHandler);
                        e.bind("mouseleave", {settings: g.settings, element: e, $plugin: g}, g.mouseOutHandler)
                    } else {
                        if (g.settings.trigger == "focus") {
                            e.bind("focus", {settings: g.settings, element: e, $plugin: g}, g.mouseOverHandler);
                            e.bind("blur", {settings: g.settings, element: e, $plugin: g}, g.mouseOutHandler)
                        } else {
                            if (g.settings.trigger == "click") {
                                this.toggle = false;
                                e.bind("click", {
                                    settings: g.settings,
                                    element: e,
                                    $plugin: g,
                                    $toggle: this.toggle
                                }, g.mouseOverHandler);
                                if (!g.settings.issticky) {
                                    e.bind("mouseleave", {
                                        settings: g.settings,
                                        element: e,
                                        $plugin: g,
                                        $toggle: this.toggle
                                    }, g.mouseOutHandler)
                                }
                            }
                        }
                    }
                }
            }
        })
    };

    function b(d, c) {
        this.settings = this.getSettings(d, c);
        this.$element = c;
        return this
    }

    b.prototype = {
        getSettings: function (f, d) {
            var e = (d.data("issticky") != null) ? ((d.data("issticky") == "true") ? true : false) : true;
            var c = a.extend({}, f, {
                location: d.data("location"),
                title: d.data("title"),
                backcolor: d.data("backcolor"),
                textalign: d.data("textalign"),
                trigger: d.data("trigger"),
                textcolor: d.data("textcolor"),
                opacity: d.data("opacity"),
                templatename: d.data("templatename"),
                width: d.data("width"),
                margin: d.data("margin"),
                padding: d.data("padding"),
                delay: d.data("delay"),
                issticky: e,
                container: d.data("container"),
                shadow: d.data("shadow")
            });
            return c
        }, mouseOverHandler: function (n) {
            if (typeof n.data.settings.onUpdate == "function") {
                n.data.settings.title = n.data.settings.onUpdate.call(this)
            }
            if (n.data.element.is("input")) {
                if (n.data.element.val() != "") {
                    return false
                }
            }
            if (n.data.settings.trigger == "click") {
                if (!n.data.$toggle) {
                    n.data.$toggle = true;
                    this.toggle = true;
                    n.data.element.unbind("click");
                    n.data.element.bind("click", {
                        settings: n.data.settings,
                        element: n.data.element,
                        $plugin: n.data.$plugin,
                        $toggle: n.data.$toggle
                    }, n.data.$plugin.mouseOutHandler)
                } else {
                    n.data.$toggle = false;
                    this.toggle = false;
                    return false
                }
            }
            var c = n.data.element;
            var d = n.data.settings;
            var R = parseInt(d.margin.toString().replace("px", ""));
            var T = parseInt(d.padding.toString().replace("px", ""));
            var Y = parseInt(d.width.toString().replace("px", ""));
            var Q = d.container == "body" ? d.location : "none";
            var N = d.backcolor;
            var X = d.textcolor;
            var W = d.textalign;
            var V = d.templatename;
            var P = d.delay;
            var K = a(d.template);
            K.css({opacity: d.opacity});
            K.css("visibility", "visible");
            K.find(".tooltip-content").css({background: N, "text-align": W}).html(d.title + d.clearfix);
            K.find(".tooltip-content").css({color: X, padding: T + "px"});
            if (d.shadow == 1) {
                K.find(".tooltip-content").css({"box-shadow": "1px 1px 3px 0px #888888"})
            }
            var M = Q;
            var L = Q.split("-")[0];
            var E = M;
            var D = L;
            K.removeClass(Q).addClass(M);
            K.find(".tooltip-arrow").removeClass(Q).addClass(M).css("border-" + L + "-color", N);
            var l = d.container;
            if (d.container != "body") {
                K.addClass("incontainer");
                l = "#" + d.container;
                a(l).children().each(function () {
                    a(this).remove()
                })
            } else {
                K.removeClass("incontainer");
                l = "body"
            }
            a(l).append(K);
            if (n.data.settings.trigger == "click") {
                var O = a('<div id="tooltip-clickoutside"></div>');
                O.css({
                    width: "100%",
                    height: "100%",
                    position: "absolute",
                    top: a(document).scrollTop() + "px",
                    left: "0px"
                });
                a("body").append(O);
                O.bind("click", {
                    settings: n.data.settings,
                    element: n.data.element,
                    $plugin: n.data.$plugin,
                    $toggle: n.data.$toggle
                }, n.data.$plugin.mouseOutHandler);
                n.data.$toggle = false;
                this.toggle = false
            } else {
                if (n.data.settings.trigger == "hoverable") {
                    n.data.element.unbind("mouseenter")
                }
            }
            if (d.container == "body") {
                K.offset({top: 0, left: 0});
                var ab = K.outerWidth();
                var Z = K.outerHeight();
                var ae = a(document).width();
                var G = scrollbarWidth();
                var ac = a(document).width() - a(window).width();
                if (ac > 0) {
                    ae = ae - G
                }
                if (ae > a(window).width()) {
                    ae = a(window).width() - G
                }
                var ad = a(document).height();
                if (ac > G) {
                    ad = ad - G
                }
                if (Y != 0) {
                    if (Y * 2 > ae) {
                        Y = Math.floor((ae / 2) - 30)
                    } else {
                        Y -= 30
                    }
                    if (Y * 1.5 > ae / 2) {
                        Y = Math.floor((ae / 2) - 30)
                    }
                } else {
                    if (340 * 2 > ae) {
                        Y = Math.floor((ae / 2) - 30)
                    } else {
                        Y = 340
                    }
                }
                K.css({"max-width": Y});
                ab = K.outerWidth();
                Z = K.outerHeight();
                var J = c.context;
                var r = J.offsetWidth;
                var o = J.offsetHeight;
                var q = c.offset().top;
                var p = c.offset().left;
                if (J.tagName.toLowerCase() == "area") {
                    var g = J.parentElement.getAttribute("name");
                    var h = J.getAttribute("shape").toLowerCase();
                    var x = a("img[usemap='#" + g + "']").offset().top;
                    var w = a("img[usemap='#" + g + "']").offset().left;
                    var j = parseInt(J.getAttribute("coords").split(",")[0]);
                    var k = parseInt(J.getAttribute("coords").split(",")[1]);
                    var i = parseInt(J.getAttribute("coords").split(",")[2]);
                    var f = parseInt(J.getAttribute("coords").split(",")[3] || i);
                    var v = {top: parseInt(x + k), left: parseInt(w + j)};
                    if (h == "circle") {
                        v = {top: parseInt(x + k - i), left: parseInt(w + j - i)};
                        i *= 2;
                        f *= 2
                    }
                    if (h == "rect") {
                        v = {top: parseInt(x + k), left: parseInt(w + j)};
                        i = i - j;
                        f = f - k
                    }
                    if (h == "poly") {
                        var m = new Array();
                        var H = J.getAttribute("coords").split(",");
                        for (var y = 0; y < H.length;) {
                            m.push({x: parseInt(H[y]), y: parseInt(H[y + 1])});
                            y = y + 2
                        }
                        m.sort(function (e, af) {
                            var ag = e.x, ah = af.x;
                            if (ag == ah) {
                                return 0
                            }
                            return ag < ah ? 1 : -1
                        });
                        var z = m[0].x;
                        m.sort(function (e, af) {
                            var ag = e.y, ah = af.y;
                            if (ag == ah) {
                                return 0
                            }
                            return ag < ah ? 1 : -1
                        });
                        var A = m[0].y;
                        m.sort(function (e, af) {
                            var ag = e.x, ah = af.x;
                            if (ag == ah) {
                                return 0
                            }
                            return ag > ah ? 1 : -1
                        });
                        var B = m[0].x;
                        m.sort(function (e, af) {
                            var ag = e.y, ah = af.y;
                            if (ag == ah) {
                                return 0
                            }
                            return ag > ah ? 1 : -1
                        });
                        var C = m[0].y;
                        v = {top: parseInt(x + C), left: parseInt(w + B)};
                        i = z - B;
                        f = A - C
                    }
                    p = v.left;
                    q = v.top;
                    r = i;
                    o = f
                }
                p = Math.round(p);
                q = Math.round(q);
                r = Math.round(r);
                o = Math.round(o);
                K.offset({top: 0, left: 0});
                var S;
                switch (Q) {
                    case "top":
                        S = {top: (q - Z - R), left: p - (ab / 2) + (r / 2)};
                        break;
                    case "top-left":
                        S = {top: (q - Z - R), left: p};
                        break;
                    case "top-right":
                        S = {top: (q - Z - R), left: p - ab + r};
                        break;
                    case "right":
                        S = {top: (q + (o / 2) - (Z / 2)), left: p + r + R};
                        break;
                    case "right-top":
                        S = {top: (q + o - Z + 8), left: p + r + R};
                        break;
                    case "right-bottom":
                        S = {top: q - 8, left: p + r + R};
                        break;
                    case "bottom":
                        S = {top: (q + o + R), left: p - (ab / 2) + (r / 2)};
                        break;
                    case "bottom-left":
                        S = {top: (q + o + R), left: p};
                        break;
                    case "bottom-right":
                        S = {top: (q + o + R), left: p - ab + r};
                        break;
                    case "left":
                        S = {top: (q + (o / 2) - (Z / 2)), left: p - ab - R};
                        break;
                    case "left-top":
                        S = {top: (q + o - Z + 8), left: p - ab - R};
                        break;
                    case "left-bottom":
                        S = {top: q - 8, left: p - ab - R};
                        break
                }
                var F = {top: 0, left: 0};
                F.left = S.left;
                F.top = S.top;
                var aa = (((M.match("bottom") != null) || (M == "left") || (M == "right")) ? (((M == "left") || (M == "right")) ? (Z / 2) : (Z)) > (ad - q - o) : false);
                if ((S.left < 0) || (S.top < 0) || (S.left + ab > ae) || aa) {
                    if (L == "top" || L == "bottom" || L == "left" || L == "right") {
                        var u = false;
                        switch (L) {
                            case "top":
                                S.top = q - Z - R;
                                S.left = p - (ab / 2) + (r / 2);
                                u = true;
                                break;
                            case "bottom":
                                S.top = q - Z - R;
                                S.left = p - (ab / 2) + (r / 2);
                                u = true;
                                break;
                            case "left":
                                var I = M.replace(L + "-", "");
                                if (I == "top") {
                                    L = "top";
                                    M = "top-left";
                                    K.removeClass(E).addClass(M);
                                    K.find(".tooltip-arrow").removeClass(E).css("border-" + D + "-color", "").addClass(M).css("border-" + L + "-color", N);
                                    D = "top";
                                    E = "top-left";
                                    K.removeClass(Q).addClass(M);
                                    K.find(".tooltip-arrow").removeClass(Q).addClass(M).css("border-" + L + "-color", N);
                                    ab = K.outerWidth();
                                    Z = K.outerHeight();
                                    S.top = q - Z - R;
                                    S.left = p - (ab / 2) + (r / 2);
                                    F.left = p;
                                    F.top = q - Z - R;
                                    aa = (((M.match("bottom") != null) || (M == "left") || (M == "right")) ? (((M == "left") || (M == "right")) ? (Z / 2) : (Z)) > (ad - q - o) : false);
                                    if ((S.left < 0) || (S.top < 0) || (S.left + ab > ae) || aa) {
                                        u = true
                                    } else {
                                        S.left = F.left;
                                        S.top = F.top
                                    }
                                } else {
                                    if (I == "bottom") {
                                        L = "bottom";
                                        M = "bottom-left";
                                        K.removeClass(E).addClass(M);
                                        K.find(".tooltip-arrow").removeClass(E).css("border-" + D + "-color", "").addClass(M).css("border-" + L + "-color", N);
                                        D = "bottom";
                                        E = "bottom-left";
                                        K.removeClass(Q).addClass(M);
                                        K.find(".tooltip-arrow").removeClass(Q).addClass(M).css("border-" + L + "-color", N);
                                        ab = K.outerWidth();
                                        Z = K.outerHeight();
                                        S.top = q + o + R;
                                        S.left = p - (ab / 2) + (r / 2);
                                        F.left = p;
                                        F.top = q + o + R;
                                        aa = (((M.match("bottom") != null) || (M == "left") || (M == "right")) ? (((M == "left") || (M == "right")) ? (Z / 2) : (Z)) > (ad - q - o) : false);
                                        if ((S.left < 0) || (S.top < 0) || (S.left + ab > ae) || aa) {
                                            u = true
                                        } else {
                                            S.left = F.left;
                                            S.top = F.top
                                        }
                                    } else {
                                        L = "top";
                                        M = "top";
                                        K.removeClass(E).addClass(M);
                                        K.find(".tooltip-arrow").removeClass(E).css("border-" + D + "-color", "").addClass(M).css("border-" + L + "-color", N);
                                        D = "top";
                                        E = "top";
                                        K.removeClass(Q).addClass(M);
                                        K.find(".tooltip-arrow").removeClass(Q).addClass(M).css("border-" + L + "-color", N);
                                        ab = K.outerWidth();
                                        Z = K.outerHeight();
                                        S.top = q - Z - R;
                                        S.left = p - (ab / 2) + (r / 2);
                                        F.left = S.left;
                                        F.top = S.top;
                                        aa = (((M.match("bottom") != null) || (M == "left") || (M == "right")) ? (((M == "left") || (M == "right")) ? (Z / 2) : (Z)) > (ad - q - o) : false);
                                        if ((S.left < 0) || (S.top < 0) || (S.left + ab > ae) || aa) {
                                            u = true
                                        } else {
                                            S.left = F.left;
                                            S.top = F.top
                                        }
                                    }
                                }
                                break;
                            case "right":
                                var I = M.replace(L + "-", "");
                                if (I == "top") {
                                    L = "top";
                                    M = "top-left";
                                    K.removeClass(E).addClass(M);
                                    K.find(".tooltip-arrow").removeClass(E).css("border-" + D + "-color", "").addClass(M).css("border-" + L + "-color", N);
                                    D = "top";
                                    E = "top-left";
                                    K.removeClass(Q).addClass(M);
                                    K.find(".tooltip-arrow").removeClass(Q).addClass(M).css("border-" + L + "-color", N);
                                    ab = K.outerWidth();
                                    Z = K.outerHeight();
                                    S.top = q - Z - R;
                                    S.left = p - (ab / 2) + (r / 2);
                                    F.left = p;
                                    F.top = q - Z - R;
                                    aa = (((M.match("bottom") != null) || (M == "left") || (M == "right")) ? (((M == "left") || (M == "right")) ? (Z / 2) : (Z)) > (ad - q - o) : false);
                                    if ((S.left < 0) || (S.top < 0) || (S.left + ab > ae) || aa) {
                                        u = true
                                    } else {
                                        S.left = F.left;
                                        S.top = F.top
                                    }
                                } else {
                                    if (I == "bottom") {
                                        L = "bottom";
                                        M = "bottom-left";
                                        K.removeClass(E).addClass(M);
                                        K.find(".tooltip-arrow").removeClass(E).css("border-" + D + "-color", "").addClass(M).css("border-" + L + "-color", N);
                                        D = "bottom";
                                        E = "bottom-left";
                                        K.removeClass(Q).addClass(M);
                                        K.find(".tooltip-arrow").removeClass(Q).addClass(M).css("border-" + L + "-color", N);
                                        ab = K.outerWidth();
                                        Z = K.outerHeight();
                                        S.top = q - Z - R;
                                        S.left = p - (ab / 2) + (r / 2);
                                        F.left = p;
                                        F.top = q + o + R;
                                        aa = (((M.match("bottom") != null) || (M == "left") || (M == "right")) ? (((M == "left") || (M == "right")) ? (Z / 2) : (Z)) > (ad - q - o) : false);
                                        if ((S.left < 0) || (S.top < 0) || (S.left + ab > ae) || aa) {
                                            u = true
                                        } else {
                                            S.left = F.left;
                                            S.top = F.top
                                        }
                                    } else {
                                        L = "top";
                                        M = "top";
                                        K.removeClass(E).addClass(M);
                                        K.find(".tooltip-arrow").removeClass(E).css("border-" + D + "-color", "").addClass(M).css("border-" + L + "-color", N);
                                        D = "top";
                                        E = "top";
                                        K.removeClass(Q).addClass(M);
                                        K.find(".tooltip-arrow").removeClass(Q).addClass(M).css("border-" + L + "-color", N);
                                        ab = K.outerWidth();
                                        Z = K.outerHeight();
                                        S.top = q - Z - R;
                                        S.left = p - (ab / 2) + (r / 2);
                                        F.left = S.left;
                                        F.top = S.top;
                                        aa = (((M.match("bottom") != null) || (M == "left") || (M == "right")) ? (((M == "left") || (M == "right")) ? (Z / 2) : (Z)) > (ad - q - o) : false);
                                        if ((S.left < 0) || (S.top < 0) || (S.left + ab > ae) || aa) {
                                            u = true
                                        } else {
                                            S.left = F.left;
                                            S.top = F.top
                                        }
                                    }
                                }
                                break
                        }
                        if (u) {
                            var s = false;
                            var t = false;
                            if (S.top < 0) {
                                L = "bottom";
                                M = "bottom";
                                S.top = q + o + R;
                                t = true;
                                if (S.left < 0) {
                                    L = "bottom";
                                    M = "bottom-left";
                                    S.left = p;
                                    s = true
                                }
                                if (S.left + ab > ae) {
                                    S.left = p - ab + r;
                                    if (S.left < 0) {
                                        L = "bottom";
                                        M = "bottom";
                                        S.left = p - (ab / 2) + (r / 2);
                                        s = true
                                    } else {
                                        L = "bottom";
                                        M = "bottom-right";
                                        S.left = p - ab + r;
                                        s = true
                                    }
                                }
                            } else {
                                L = "top";
                                M = "top";
                                S.top = q - Z - R;
                                t = false;
                                if (S.left < 0) {
                                    L = "top";
                                    M = "top-left";
                                    S.left = p;
                                    s = true
                                }
                                if (S.left + ab > ae) {
                                    S.left = p - ab + r;
                                    if (S.left < 0) {
                                        L = "top";
                                        M = "top";
                                        S.left = p - (ab / 2) + (r / 2);
                                        s = true
                                    } else {
                                        L = "top";
                                        M = "top-right";
                                        S.left = p - ab + r;
                                        s = true
                                    }
                                }
                            }
                            if (!s) {
                                if (t) {
                                    M = E.replace("top", "bottom");
                                    L = D.replace("top", "bottom");
                                    if (F.left < 0) {
                                        if (L == "bottom" || L == "top") {
                                            M = M.replace("right", "left");
                                            S.left = p
                                        }
                                    } else {
                                        S.left = F.left
                                    }
                                } else {
                                    M = E.replace("bottom", "top");
                                    L = D.replace("bottom", "top");
                                    if (F.left < 0) {
                                        if (L == "bottom" || L == "top") {
                                            M = M.replace("right", "left");
                                            S.left = p
                                        }
                                    } else {
                                        S.left = F.left
                                    }
                                }
                            }
                        }
                    }
                }
                K.removeClass(E).addClass(M);
                K.find(".tooltip-arrow").removeClass(E).css("border-" + D + "-color", "").addClass(M).css("border-" + L + "-color", N);
                if (V != "") {
                    if (K.find(".tooltip-content > .template").hasClass("template")) {
                        K.find(".tooltip-content > .template").addClass(V);
                        var U = K.find("." + V).css("background-color");
                        K.find(".tooltip-arrow").css("border-" + D + "-color", "");
                        K.find(".tooltip-arrow").css("border-" + L + "-color", U);
                        K.find(".tooltip-content").css({background: U})
                    } else {
                        if (K.find(".tooltip-content > .tooltip-menu").hasClass("tooltip-menu")) {
                            K.find(".tooltip-content > .tooltip-menu").addClass(V);
                            var U = K.find("." + V).css("background-color");
                            K.find(".tooltip-arrow").css("border-" + D + "-color", "");
                            K.find(".tooltip-arrow").css("border-" + L + "-color", U);
                            K.find(".tooltip-content").css({background: U})
                        }
                    }
                }
                K.find(".tooltip-content > .video-wrapper").css({width: (K.width() - (T * 2)) + "px"});
                K.offset(S)
            }
            K.hide();
            c.removeAttr("title");
            c.removeAttr("alt");
            if (n.data.settings.trigger == "hoverable" || n.data.settings.trigger == "click") {
                P = 0
            }
            switch (L) {
                case "top":
                    K.delay(P).css({top: "-=20", opacity: 0, display: "block"}).stop(true, true).animate({
                        top: "+=20",
                        opacity: d.opacity
                    }, 150);
                    break;
                case "bottom":
                    K.delay(P).css({top: "+=20", opacity: 0, display: "block"}).stop(true, true).animate({
                        top: "-=20",
                        opacity: d.opacity
                    }, 150);
                    break;
                case "left":
                    K.delay(P).css({left: "-=20", opacity: 0, display: "block"}).stop(true, true).animate({
                        left: "+=20",
                        opacity: d.opacity
                    }, 150);
                    break;
                case "right":
                    K.delay(P).css({left: "+=20", opacity: 0, display: "block"}).stop(true, true).animate({
                        left: "-=20",
                        opacity: d.opacity
                    }, 150);
                    break;
                default:
                    K.delay(P).css({opacity: 0, display: "block"}).stop(true, true).animate({opacity: d.opacity}, 150);
                    break
            }
            n.data.$plugin.tooltip = K;
            n.data.$plugin.location = Q;
            n.data.$plugin.tooltip_arrow_border = L;
            K = null;
            return false
        }, mouseOutHandler: function (d) {
            var f = d.data.$plugin.tooltip;
            var g = d.data.$plugin.location;
            var c = false;
            if (d.data.settings.trigger != "hoverable") {
                if (d.data.settings.trigger == "hover") {
                    a(f).delay(d.data.settings.delay);
                    c = true
                } else {
                    c = true;
                    if (d.data.settings.trigger == "click") {
                        if (!d.data.settings.issticky) {
                            d.data.settings.interval = setInterval(function () {
                                a(f).fadeOut(0, function () {
                                    a(d.data.$plugin.tooltip).remove()
                                });
                                clearInterval(d.data.settings.interval);
                                this.toggle = false;
                                d.data.$toggle = false;
                                d.data.element.unbind("click");
                                d.data.element.unbind("mouseleave");
                                d.data.element.bind("click", {
                                    settings: d.data.settings,
                                    element: d.data.element,
                                    $plugin: d.data.$plugin,
                                    $toggle: false
                                }, d.data.$plugin.mouseOverHandler);
                                d.data.element.bind("mouseleave", {
                                    settings: d.data.settings,
                                    element: d.data.element,
                                    $plugin: d.data.$plugin,
                                    $toggle: false
                                }, d.data.$plugin.mouseOutHandler)
                            }, d.data.settings.delay == 0 ? 2000 : d.data.settings.delay);
                            d.data.element.unbind("mouseleave");
                            a(f).find(".tooltip-content").bind("mouseenter", {
                                settings: d.data.settings,
                                element: d.data.element,
                                $plugin: d.data.$plugin,
                                $toggle: true
                            }, function () {
                                d.data.element.unbind("click");
                                d.data.element.unbind("mouseleave");
                                this.toggle = true;
                                d.data.$toggle = true;
                                clearInterval(d.data.settings.interval)
                            });
                            a(f).find(".tooltip-content").bind("mouseleave", {
                                settings: d.data.settings,
                                element: d.data.element,
                                $plugin: d.data.$plugin,
                                $toggle: d.data.$toggle
                            }, function () {
                                a(f).fadeOut(0, function () {
                                    a(d.data.$plugin.tooltip).remove()
                                });
                                this.toggle = false;
                                d.data.$toggle = false;
                                d.data.element.unbind("click");
                                d.data.element.unbind("mouseleave");
                                d.data.element.bind("click", {
                                    settings: d.data.settings,
                                    element: d.data.element,
                                    $plugin: d.data.$plugin,
                                    $toggle: false
                                }, d.data.$plugin.mouseOverHandler);
                                d.data.element.bind("mouseleave", {
                                    settings: d.data.settings,
                                    element: d.data.element,
                                    $plugin: d.data.$plugin,
                                    $toggle: false
                                }, d.data.$plugin.mouseOutHandler)
                            });
                            c = false
                        } else {
                            c = true
                        }
                    }
                }
            } else {
                d.data.settings.interval = setInterval(function () {
                    a(f).fadeOut(0, function () {
                        a(d.data.$plugin.tooltip).remove()
                    });
                    clearInterval(d.data.settings.interval);
                    d.data.element.unbind("mouseleave");
                    d.data.element.unbind("mouseenter");
                    d.data.element.bind("mouseenter", {
                        settings: d.data.settings,
                        element: d.data.element,
                        $plugin: d.data.$plugin,
                        $toggle: false
                    }, d.data.$plugin.mouseOverHandler);
                    d.data.element.bind("mouseleave", {
                        settings: d.data.settings,
                        element: d.data.element,
                        $plugin: d.data.$plugin,
                        $toggle: false
                    }, d.data.$plugin.mouseOutHandler)
                }, d.data.settings.delay == 0 ? 2000 : d.data.settings.delay);
                d.data.element.unbind("mouseleave");
                a(f).find(".tooltip-content").bind("mouseenter", {
                    settings: d.data.settings,
                    element: d.data.element,
                    $plugin: d.data.$plugin,
                    $toggle: true
                }, function () {
                    d.data.element.unbind("mouseenter");
                    d.data.element.unbind("mouseleave");
                    this.toggle = true;
                    d.data.$toggle = true;
                    clearInterval(d.data.settings.interval)
                });
                a(f).find(".tooltip-content").bind("mouseleave", {
                    settings: d.data.settings,
                    element: d.data.element,
                    $plugin: d.data.$plugin,
                    $toggle: true
                }, function () {
                    a(f).fadeOut(0, function () {
                        a(d.data.$plugin.tooltip).remove()
                    });
                    this.toggle = false;
                    d.data.$toggle = false;
                    d.data.element.unbind("mouseleave");
                    d.data.element.unbind("mouseenter");
                    d.data.element.bind("mouseenter", {
                        settings: d.data.settings,
                        element: d.data.element,
                        $plugin: d.data.$plugin,
                        $toggle: false
                    }, d.data.$plugin.mouseOverHandler);
                    d.data.element.bind("mouseleave", {
                        settings: d.data.settings,
                        element: d.data.element,
                        $plugin: d.data.$plugin,
                        $toggle: false
                    }, d.data.$plugin.mouseOutHandler)
                });
                c = false
            }
            if (c) {
                switch (d.data.$plugin.tooltip_arrow_border) {
                    case "top":
                        a(f).stop(true, true).animate({top: "-=20", opacity: 0}, 150, function () {
                            a(d.data.$plugin.tooltip).remove()
                        });
                        break;
                    case "bottom":
                        a(f).stop(true, true).animate({top: "+=20", opacity: 0}, 150, function () {
                            a(d.data.$plugin.tooltip).remove()
                        });
                        break;
                    case "left":
                        a(f).stop(true, true).animate({left: "-=20", opacity: 0}, 150, function () {
                            a(d.data.$plugin.tooltip).remove()
                        });
                        break;
                    case "right":
                        a(f).stop(true, true).animate({left: "+=20", opacity: 0}, 150, function () {
                            a(d.data.$plugin.tooltip).remove()
                        });
                        break
                }
                a(d.data.$plugin.tooltip).remove()
            }
            if (d.data.settings.trigger == "click") {
                if (d.data.$toggle) {
                    a("body").find("#tooltip-clickoutside").remove();
                    this.toggle = false;
                    d.data.$toggle = false;
                    d.data.element.unbind("click");
                    d.data.element.unbind("mouseleave");
                    d.data.element.bind("click", {
                        settings: d.data.settings,
                        element: d.data.element,
                        $plugin: d.data.$plugin,
                        $toggle: d.data.$toggle
                    }, d.data.$plugin.mouseOverHandler);
                    if (!d.data.settings.issticky) {
                        d.data.element.bind("mouseleave", {
                            settings: d.data.settings,
                            element: d.data.element,
                            $plugin: d.data.$plugin,
                            $toggle: d.data.$toggle
                        }, d.data.$plugin.mouseOutHandler)
                    }
                }
            }
            return false
        }
    };
    scrollbarWidth = function () {
        var c = a('<div style="width:50px;height:50px;overflow:hidden;position:absolute;top:-200px;left:-200px;"><div style="height:100px;"></div>');
        a("body").append(c);
        var d = a("div", c).innerWidth();
        c.css("overflow", "scroll");
        var e = a("div", c).innerWidth();
        a(c).remove();
        return (d - e)
    };
    a.fn.LiteTooltip.defaultSettings = {
        location: "top",
        title: "",
        opacity: 0.89,
        backcolor: "#000000",
        textcolor: "#ffffff",
        template: '<div class="litetooltip-wrapper"><div class="tooltip-arrow"></div><div class="tooltip-content"></div></div>',
        margin: 5,
        padding: 10,
        width: 0,
        textalign: "center",
        trigger: "hover",
        templatename: "",
        delay: 0,
        issticky: true,
        clearfix: '<div class="clear"></div>',
        container: "body",
        shadow: 1
    }
})(jQuery);
$(document).ready(function () {
    $("#hotspot-properties-modal").css({
        width: (80 * $(window).width()) / 100,
        "margin-left": 0,
        left: (10 * $(window).width()) / 100
    })
});

function loadImage() {
    $("#map-area").html("");
    var a = $("<div></div>");
    a.appendTo($("#map-area"));
    var b = $('<img src="' + $("#txtHotspotImage").val() + '" />');
    b.css({border: "1px solid #ffffff"});
    b.appendTo(a);
    b.load(function () {
        $("#map-area").css({width: $(this).width() + 2});
        var c = ($(this).height() / $(this).width()) * 100;
        $(this).attr("data-width", $(this).width());
        $(this).attr("data-height", $(this).height());
        a.css({position: "relative", height: "0px", "padding-bottom": c + "%"})
    })
}

$("#map-area").mousedown(function (a) {
    var c = {X: 0, Y: 0};
    if (a.offsetX == undefined) {
        c = {X: a.pageX - $(this).offset().left - 16, Y: a.pageY - $(this).offset().top - 16}
    } else {
        c = {X: a.offsetX - 16, Y: a.offsetY - 16}
    }
    var g = $.now();
    var f = "selector_" + g;
    var d = "hotspot_" + g;
    var b = $('<div class="selector" id="' + f + '"><div id="' + d + '" class="hotspot ui-widget-content"><div class="data-container"></div></div></div>');
    b.css({position: "absolute", top: c.Y, left: c.X, border: "dashed 2px #bbbbbb", padding: "5px"});
    b.find(".hotspot").css({
        background: "#cc0000",
        width: "20px",
        height: "20px",
        "border-radius": "20px",
        opacity: 0.8
    });
    b.resizable({alsoResize: b.find(".hotspot"), containment: "parent"});
    b.draggable({
        containment: "parent", scroll: false, start: function () {
            changeSelection(this)
        }
    });
    b.appendTo(this);
    b.mousedown(function () {
        changeSelection(this);
        return false
    });
    b.dblclick(function () {
        setProperties(this);
        return false
    });
    b.on('doubletap', function () {
        setProperties(this);
        return false
    })
});

function saveHotspot() {
    var a = "#" + $("#data_id").val();
    var c = $(a).clone();
    $(c).appendTo($(a).parent());
    $(a).remove();
    var d = $.now();
    var b = "hotspot_" + d;
    $(c).attr("id", b);
    $("#data_id").val(b);
    a = "#" + $("#data_id").val();
    $(a).parent().resizable({alsoResize: $(a)});
    $(a).find(".data-container").html($("#data_content").val());
    $(a).data("location", $("#data_location").val());
    if ($("#data_template").val() != "default") {
        $(a).data("template", $("#data_template").val())
    }
    if ($("#data_templatename").val() != "default") {
        $(a).data("templatename", $("#data_templatename").val())
    }
    $(a).data("opacity", $("#data_opacity").val());
    $(a).data("backcolor", $("#data_backcolor").val());
    $(a).data("textcolor", $("#data_textcolor").val());
    $(a).data("textalign", $("#data_textalign").val());
    $(a).data("margin", $("#data_margin").val());
    $(a).data("padding", $("#data_padding").val());
    $(a).data("width", $("#data_width").val());
    $(a).data("delay", $("#data_delay").val());
    $(a).data("trigger", $("#data_trigger").val());
    $(a).data("issticky", $("#data_issticky").val());
    $(a).data("hotspot-blink", $("#data_h_blink").val());
    $(a).data("hotspot-bgcolor", $("#data_h_bgcolor").val());
    $(a).data("hotspot-bordercolor", $("#data_h_bordercolor").val());
    $(a).data("hotspot-borderradius", $("#data_h_borderradius").val());
    $(a).css({
        background: $("#data_h_bgcolor").val(),
        border: "1px solid " + $("#data_h_bordercolor").val(),
        "border-radius": $("#data_h_borderradius").val() + "px"
    });
    $(a).LiteTooltip({title: getDataTitle(a)});
    generateCode();
    $("#hotspot-properties-modal").modal("hide")
}

function getDataTitle(a) {
    return $(a).find(".data-container").html()
}

function changeSelection(a) {
    $("#map-area").find(".selector").each(function () {
        $(this).css({"border-color": "#bbbbbb", background: "none"})
    });
    $(a).css({"border-color": "#111111", background: "rgba(255, 255, 255, 0.35)"})
}

function setProperties(a) {
    a = $(a).find(".hotspot");
    $("#data_id").val(a.attr("id"));
    $("#data_content").val(a.find(".data-container").html());
    $("#data_location").val(a.data("location") != null ? a.data("location") : "top");
    $("#data_template").val(a.data("template") != null ? a.data("template") : "default");
    $("#data_templatename").val(a.data("templatename") != null ? a.data("templatename") : "default");
    $("#data_opacity").val(a.data("opacity") != null ? a.data("opacity") : 0.8);
    $("#data_backcolor").val(a.data("backcolor") != null ? a.data("backcolor") : "#000000");
    $("#data_textcolor").val(a.data("textcolor") != null ? a.data("textcolor") : "#ffffff");
    $("#data_textalign").val(a.data("textalign") != null ? a.data("textalign") : "center");
    $("#data_margin").val(a.data("margin") != null ? a.data("margin") : 5);
    $("#data_padding").val(a.data("padding") != null ? a.data("padding") : 10);
    $("#data_width").val(a.data("width") != null ? a.data("width") : 0);
    $("#data_delay").val(a.data("delay") != null ? a.data("delay") : 0);
    $("#data_trigger").val(a.data("trigger") != null ? a.data("trigger") : "hover");
    $("#data_issticky").val(a.data("issticky") != null ? String(a.data("issticky")) : "true");
    $("#data_h_blink").val(a.data("hotspot-blink") != null ? String(a.data("hotspot-blink")) : "true");
    $("#data_h_bgcolor").val(a.data("hotspot-bgcolor") != null ? a.data("hotspot-bgcolor") : "#cc0000");
    $("#data_h_bordercolor").val(a.data("hotspot-bordercolor") != null ? a.data("hotspot-bordercolor") : "#cc0000");
    $("#data_h_borderradius").val(a.data("hotspot-borderradius") != null ? a.data("hotspot-borderradius") : 20);
    $("#hotspot-properties-modal").modal("show")
}

function generateCode() {
    var d = $("#map-area").find("img").attr("src");
    if (d == null) {
        return
    }
    var e = $("#map-area").find("img").width();
    var c = $("#map-area").find("img").height();
    $("#preview").css({width: e});
    var f = ($("#map-area").find("img").height() / $("#map-area").find("img").width()) * 100;
    var a = "";
    a = '<div class="litetooltip-hotspot-wrapper" style="max-width: ' + e + 'px">\n';
    a += '<div class="litetooltip-hotspot-container" style="padding-bottom: ' + f + '%">\n';
    a += '<img src="' + $("#map-area").find("img").attr("src") + '" data-width="' + e + '" data-height="' + c + '" />\n';
    $("#map-area").find(".hotspot").each(function () {
        var g = $(this);
        var n = ((g.parent().position().left + 6) / e) * 100;
        var o = ((g.parent().position().top + 6) / c) * 100;
        var q = (g.width() / e) * 100;
        var m = (g.height() / c) * 100;
        var i = g.data("hotspot-bgcolor");
        var k = "1px solid " + g.data("hotspot-bordercolor");
        var l = g.data("hotspot-borderradius");
        var p = 0.8;
        var j = String(g.data("hotspot-blink")) == "true" ? " blink" : "";
        var h = '<div class="hotspot' + j + '" style="top: ' + o + "%; left: " + n + "%; width: " + q + "%; height: " + m + "%; background: " + i + "; border: " + k + "; border-radius: " + l + "px; opacity: " + p + '" id="' + g.attr("id") + '" data-location="' + g.data("location") + '" data-template="' + (g.data("template") != null ? g.data("template") : "") + '" data-templatename="' + (g.data("templatename") != null ? g.data("templatename") : "") + '" data-opacity="' + g.data("opacity") + '" data-backcolor="' + g.data("backcolor") + '" data-textcolor="' + g.data("textcolor") + '" data-textalign="' + g.data("textalign") + '" data-margin="' + g.data("margin") + '" data-padding="' + g.data("padding") + '" data-width="' + g.data("width") + '" data-delay="' + g.data("delay") + '" data-trigger="' + g.data("trigger") + '" data-issticky="' + g.data("issticky") + '" data-hotspot-x="' + n + '" data-hotspot-y="' + o + '" data-hotspot-blink="' + g.data("hotspot-blink") + '" data-hotspot-bgcolor="' + g.data("hotspot-bgcolor") + '" data-hotspot-bordercolor="' + g.data("hotspot-bordercolor") + '" data-hotspot-borderradius="' + g.data("hotspot-borderradius") + '">\n<div class="data-container">' + g.find(".data-container").html() + "</div>\n</div>\n\n";
        a += h
    });
    a += "</div>\n";
    a += "</div>";
    $("#data_code").val(a);
    $("#preview").html(a);
    $(".litetooltip-hotspot-wrapper .hotspot").each(function () {
        $(this).LiteTooltip({title: $(this).find(".data-container").html()})
    });
    var b = "$('.litetooltip-hotspot-wrapper .hotspot').each(function () { \n    $(this).LiteTooltip({ title: $(this).find('.data-container').html() });\n });\n";
    $("#data_code_jquery").html(b)
}

function reverseCode() {
    var a = $("#data_code").val();
    $("#preview").html(a);
    $("#preview .hotspot").each(function () {
        $(this).LiteTooltip({title: $(this).find(".data-container").html()})
    });
    var e = $("#preview").find(".litetooltip-hotspot-container > img").attr("src");
    if (e == null) {
        return
    }
    var f = $("#preview").find(".litetooltip-hotspot-container > img").data("width");
    var d = $("#preview").find(".litetooltip-hotspot-container > img").data("height");
    $("#txtHotspotImage").val(e);
    var c = $('<img src="' + e + '" />');
    c.css({border: "1px solid #fff"});
    c.appendTo($("#map-area"));
    var b = $("<div></div>");
    f = f != null ? f : c.width();
    d = d != null ? d : c.height();
    var g = (d / f) * 100;
    b.css({position: "relative", height: "0px", "padding-bottom": g + "%"});
    b.appendTo($("#map-area"));
    c.remove();
    c.appendTo(b);
    $("#map-area").css({width: f + 2});
    $("#preview").css({width: f + 2});
    $("#preview").find(".litetooltip-hotspot-container .hotspot").each(function (s) {
        var u = $.now();
        var t = "selector_" + u;
        var r = "hotspot_" + u;
        var h = $(this);
        var j = $('<div class="selector" id="' + t + '"><div id="' + r + '" class="hotspot ui-widget-content"><div class="data-container"></div></div></div>');
        var i = j.find(".hotspot");
        var o = ((h.data("hotspot-x") * f) / 100) - 6;
        var p = ((h.data("hotspot-y") * d) / 100) - 6;
        var q = h.width();
        var n = h.height();
        var k = h.data("hotspot-bgcolor");
        var l = "1px solid " + h.data("hotspot-bordercolor");
        var m = h.data("hotspot-borderradius");
        j.css({position: "absolute", top: p, left: o, border: "dashed 2px #bbbbbb", padding: "5px"});
        i.css({background: k, width: q, height: n, "border-radius": m, opacity: 0.8});
        i.data("location", h.data("location"));
        i.data("template", h.data("template") != "" ? h.data("template") : "default");
        i.data("templatename", h.data("templatename") != "" ? h.data("templatename") : "default");
        i.data("opacity", h.data("opacity"));
        i.data("backcolor", h.data("backcolor"));
        i.data("textcolor", h.data("textcolor"));
        i.data("textalign", h.data("textalign"));
        i.data("margin", h.data("margin"));
        i.data("padding", h.data("padding"));
        i.data("width", h.data("width"));
        i.data("delay", h.data("delay"));
        i.data("trigger", h.data("trigger"));
        i.data("issticky", h.data("issticky"));
        i.data("hotspot-blink", h.data("hotspot-blink"));
        i.data("hotspot-bgcolor", h.data("hotspot-bgcolor"));
        i.data("hotspot-bordercolor", h.data("hotspot-bordercolor"));
        i.data("hotspot-borderradius", h.data("hotspot-borderradius"));
        i.find(".data-container").html(h.find(".data-container").html());
        j.resizable({alsoResize: j.find(".hotspot"), containment: "parent"});
        j.draggable({
            containment: "parent", scroll: false, start: function () {
                changeSelection(this)
            }
        });
        j.appendTo($("#map-area"));
        j.mousedown(function () {
            changeSelection(this);
            return false
        });
        j.dblclick(function () {
            setProperties(this);
            return false
        });
        j.on('doubletap', function () {
            setProperties(this);
            return false
        });
        i.LiteTooltip({title: $(this).find(".data-container").html()})
    })
}

function deleteHotspot() {
    var a = "#" + $("#data_id").val();
    $(a).parent().remove();
    $("#data_id").val("");
    $("#data_content").val("");
    $("#data_location").val("top");
    $("#data_template").val("default");
    $("#data_templatename").val("default");
    $("#data_opacity").val(0.8);
    $("#data_backcolor").val("#000000");
    $("#data_textcolor").val("#ffffff");
    $("#data_textalign").val("center");
    $("#data_margin").val(5);
    $("#data_padding").val(10);
    $("#data_width").val(0);
    $("#data_delay").val(0);
    $("#data_trigger").val("hover");
    $("#data_issticky").val("true");
    $("#data_h_blink").val("true");
    $("#data_h_bgcolor").val("#cc0000");
    $("#data_h_bordercolor").val("#cc0000");
    $("#data_h_borderradius").val(20);
    generateCode()
}

$("#btn_data_image").click(function () {
    loadImage()
});
$("#btn_data_save").click(function () {
    saveHotspot()
});
$("#btn_data_update").click(function () {
    generateCode()
});
$("#btn_data_delete").click(function () {
    deleteHotspot()
});
$("#btn_data_reverse").click(function () {
    reverseCode()
});
var q = null;
window.PR_SHOULD_USE_CONTINUATION = !0;
(function () {
    function L(a) {
        function m(a) {
            var f = a.charCodeAt(0);
            if (f !== 92) return f;
            var b = a.charAt(1);
            return (f = r[b]) ? f : "0" <= b && b <= "7" ? parseInt(a.substring(1), 8) : b === "u" || b === "x" ? parseInt(a.substring(2), 16) : a.charCodeAt(1)
        }

        function e(a) {
            if (a < 32) return (a < 16 ? "\\x0" : "\\x") + a.toString(16);
            a = String.fromCharCode(a);
            if (a === "\\" || a === "-" || a === "[" || a === "]") a = "\\" + a;
            return a
        }

        function h(a) {
            for (var f = a.substring(1, a.length - 1).match(/\\u[\dA-Fa-f]{4}|\\x[\dA-Fa-f]{2}|\\[0-3][0-7]{0,2}|\\[0-7]{1,2}|\\[\S\s]|[^\\]/g), a =
                [], b = [], o = f[0] === "^", c = o ? 1 : 0, i = f.length; c < i; ++c) {
                var j = f[c];
                if (/\\[bdsw]/i.test(j)) a.push(j); else {
                    var j = m(j), d;
                    c + 2 < i && "-" === f[c + 1] ? (d = m(f[c + 2]), c += 2) : d = j;
                    b.push([j, d]);
                    d < 65 || j > 122 || (d < 65 || j > 90 || b.push([Math.max(65, j) | 32, Math.min(d, 90) | 32]), d < 97 || j > 122 || b.push([Math.max(97, j) & -33, Math.min(d, 122) & -33]))
                }
            }
            b.sort(function (a, f) {
                return a[0] - f[0] || f[1] - a[1]
            });
            f = [];
            j = [NaN, NaN];
            for (c = 0; c < b.length; ++c) i = b[c], i[0] <= j[1] + 1 ? j[1] = Math.max(j[1], i[1]) : f.push(j = i);
            b = ["["];
            o && b.push("^");
            b.push.apply(b, a);
            for (c = 0; c <
            f.length; ++c) i = f[c], b.push(e(i[0])), i[1] > i[0] && (i[1] + 1 > i[0] && b.push("-"), b.push(e(i[1])));
            b.push("]");
            return b.join("")
        }

        function y(a) {
            for (var f = a.source.match(/\[(?:[^\\\]]|\\[\S\s])*]|\\u[\dA-Fa-f]{4}|\\x[\dA-Fa-f]{2}|\\\d+|\\[^\dux]|\(\?[!:=]|[()^]|[^()[\\^]+/g), b = f.length, d = [], c = 0, i = 0; c < b; ++c) {
                var j = f[c];
                j === "(" ? ++i : "\\" === j.charAt(0) && (j = +j.substring(1)) && j <= i && (d[j] = -1)
            }
            for (c = 1; c < d.length; ++c) -1 === d[c] && (d[c] = ++t);
            for (i = c = 0; c < b; ++c) j = f[c], j === "(" ? (++i, d[i] === void 0 && (f[c] = "(?:")) : "\\" === j.charAt(0) &&
                (j = +j.substring(1)) && j <= i && (f[c] = "\\" + d[i]);
            for (i = c = 0; c < b; ++c) "^" === f[c] && "^" !== f[c + 1] && (f[c] = "");
            if (a.ignoreCase && s) for (c = 0; c < b; ++c) j = f[c], a = j.charAt(0), j.length >= 2 && a === "[" ? f[c] = h(j) : a !== "\\" && (f[c] = j.replace(/[A-Za-z]/g, function (a) {
                a = a.charCodeAt(0);
                return "[" + String.fromCharCode(a & -33, a | 32) + "]"
            }));
            return f.join("")
        }

        for (var t = 0, s = !1, l = !1, p = 0, d = a.length; p < d; ++p) {
            var g = a[p];
            if (g.ignoreCase) l = !0; else if (/[a-z]/i.test(g.source.replace(/\\u[\da-f]{4}|\\x[\da-f]{2}|\\[^UXux]/gi, ""))) {
                s = !0;
                l = !1;
                break
            }
        }
        for (var r =
            {b: 8, t: 9, n: 10, v: 11, f: 12, r: 13}, n = [], p = 0, d = a.length; p < d; ++p) {
            g = a[p];
            if (g.global || g.multiline) throw Error("" + g);
            n.push("(?:" + y(g) + ")")
        }
        return RegExp(n.join("|"), l ? "gi" : "g")
    }

    function M(a) {
        function m(a) {
            switch (a.nodeType) {
                case 1:
                    if (e.test(a.className)) break;
                    for (var g = a.firstChild; g; g = g.nextSibling) m(g);
                    g = a.nodeName;
                    if ("BR" === g || "LI" === g) h[s] = "\n", t[s << 1] = y++, t[s++ << 1 | 1] = a;
                    break;
                case 3:
                case 4:
                    g = a.nodeValue, g.length && (g = p ? g.replace(/\r\n?/g, "\n") : g.replace(/[\t\n\r ]+/g, " "), h[s] = g, t[s << 1] = y, y += g.length,
                        t[s++ << 1 | 1] = a)
            }
        }

        var e = /(?:^|\s)nocode(?:\s|$)/, h = [], y = 0, t = [], s = 0, l;
        a.currentStyle ? l = a.currentStyle.whiteSpace : window.getComputedStyle && (l = document.defaultView.getComputedStyle(a, q).getPropertyValue("white-space"));
        var p = l && "pre" === l.substring(0, 3);
        m(a);
        return {a: h.join("").replace(/\n$/, ""), c: t}
    }

    function B(a, m, e, h) {
        m && (a = {a: m, d: a}, e(a), h.push.apply(h, a.e))
    }

    function x(a, m) {
        function e(a) {
            for (var l = a.d, p = [l, "pln"], d = 0, g = a.a.match(y) || [], r = {}, n = 0, z = g.length; n < z; ++n) {
                var f = g[n], b = r[f], o = void 0, c;
                if (typeof b ===
                    "string") c = !1; else {
                    var i = h[f.charAt(0)];
                    if (i) o = f.match(i[1]), b = i[0]; else {
                        for (c = 0; c < t; ++c) if (i = m[c], o = f.match(i[1])) {
                            b = i[0];
                            break
                        }
                        o || (b = "pln")
                    }
                    if ((c = b.length >= 5 && "lang-" === b.substring(0, 5)) && !(o && typeof o[1] === "string")) c = !1, b = "src";
                    c || (r[f] = b)
                }
                i = d;
                d += f.length;
                if (c) {
                    c = o[1];
                    var j = f.indexOf(c), k = j + c.length;
                    o[2] && (k = f.length - o[2].length, j = k - c.length);
                    b = b.substring(5);
                    B(l + i, f.substring(0, j), e, p);
                    B(l + i + j, c, C(b, c), p);
                    B(l + i + k, f.substring(k), e, p)
                } else p.push(l + i, b)
            }
            a.e = p
        }

        var h = {}, y;
        (function () {
            for (var e = a.concat(m),
                     l = [], p = {}, d = 0, g = e.length; d < g; ++d) {
                var r = e[d], n = r[3];
                if (n) for (var k = n.length; --k >= 0;) h[n.charAt(k)] = r;
                r = r[1];
                n = "" + r;
                p.hasOwnProperty(n) || (l.push(r), p[n] = q)
            }
            l.push(/[\S\s]/);
            y = L(l)
        })();
        var t = m.length;
        return e
    }

    function u(a) {
        var m = [], e = [];
        a.tripleQuotedStrings ? m.push(["str", /^(?:'''(?:[^'\\]|\\[\S\s]|''?(?=[^']))*(?:'''|$)|"""(?:[^"\\]|\\[\S\s]|""?(?=[^"]))*(?:"""|$)|'(?:[^'\\]|\\[\S\s])*(?:'|$)|"(?:[^"\\]|\\[\S\s])*(?:"|$))/, q, "'\""]) : a.multiLineStrings ? m.push(["str", /^(?:'(?:[^'\\]|\\[\S\s])*(?:'|$)|"(?:[^"\\]|\\[\S\s])*(?:"|$)|`(?:[^\\`]|\\[\S\s])*(?:`|$))/,
            q, "'\"`"]) : m.push(["str", /^(?:'(?:[^\n\r'\\]|\\.)*(?:'|$)|"(?:[^\n\r"\\]|\\.)*(?:"|$))/, q, "\"'"]);
        a.verbatimStrings && e.push(["str", /^@"(?:[^"]|"")*(?:"|$)/, q]);
        var h = a.hashComments;
        h && (a.cStyleComments ? (h > 1 ? m.push(["com", /^#(?:##(?:[^#]|#(?!##))*(?:###|$)|.*)/, q, "#"]) : m.push(["com", /^#(?:(?:define|elif|else|endif|error|ifdef|include|ifndef|line|pragma|undef|warning)\b|[^\n\r]*)/, q, "#"]), e.push(["str", /^<(?:(?:(?:\.\.\/)*|\/?)(?:[\w-]+(?:\/[\w-]+)+)?[\w-]+\.h|[a-z]\w*)>/, q])) : m.push(["com", /^#[^\n\r]*/,
            q, "#"]));
        a.cStyleComments && (e.push(["com", /^\/\/[^\n\r]*/, q]), e.push(["com", /^\/\*[\S\s]*?(?:\*\/|$)/, q]));
        a.regexLiterals && e.push(["lang-regex", /^(?:^^\.?|[!+-]|!=|!==|#|%|%=|&|&&|&&=|&=|\(|\*|\*=|\+=|,|-=|->|\/|\/=|:|::|;|<|<<|<<=|<=|=|==|===|>|>=|>>|>>=|>>>|>>>=|[?@[^]|\^=|\^\^|\^\^=|{|\||\|=|\|\||\|\|=|~|break|case|continue|delete|do|else|finally|instanceof|return|throw|try|typeof)\s*(\/(?=[^*/])(?:[^/[\\]|\\[\S\s]|\[(?:[^\\\]]|\\[\S\s])*(?:]|$))+\/)/]);
        (h = a.types) && e.push(["typ", h]);
        a = ("" + a.keywords).replace(/^ | $/g,
            "");
        a.length && e.push(["kwd", RegExp("^(?:" + a.replace(/[\s,]+/g, "|") + ")\\b"), q]);
        m.push(["pln", /^\s+/, q, " \r\n\t\xa0"]);
        e.push(["lit", /^@[$_a-z][\w$@]*/i, q], ["typ", /^(?:[@_]?[A-Z]+[a-z][\w$@]*|\w+_t\b)/, q], ["pln", /^[$_a-z][\w$@]*/i, q], ["lit", /^(?:0x[\da-f]+|(?:\d(?:_\d+)*\d*(?:\.\d*)?|\.\d\+)(?:e[+-]?\d+)?)[a-z]*/i, q, "0123456789"], ["pln", /^\\[\S\s]?/, q], ["pun", /^.[^\s\w"-$'./@\\`]*/, q]);
        return x(m, e)
    }

    function D(a, m) {
        function e(a) {
            switch (a.nodeType) {
                case 1:
                    if (k.test(a.className)) break;
                    if ("BR" === a.nodeName) h(a),
                    a.parentNode && a.parentNode.removeChild(a); else for (a = a.firstChild; a; a = a.nextSibling) e(a);
                    break;
                case 3:
                case 4:
                    if (p) {
                        var b = a.nodeValue, d = b.match(t);
                        if (d) {
                            var c = b.substring(0, d.index);
                            a.nodeValue = c;
                            (b = b.substring(d.index + d[0].length)) && a.parentNode.insertBefore(s.createTextNode(b), a.nextSibling);
                            h(a);
                            c || a.parentNode.removeChild(a)
                        }
                    }
            }
        }

        function h(a) {
            function b(a, d) {
                var e = d ? a.cloneNode(!1) : a, f = a.parentNode;
                if (f) {
                    var f = b(f, 1), g = a.nextSibling;
                    f.appendChild(e);
                    for (var h = g; h; h = g) g = h.nextSibling, f.appendChild(h)
                }
                return e
            }

            for (; !a.nextSibling;) if (a = a.parentNode, !a) return;
            for (var a = b(a.nextSibling, 0), e; (e = a.parentNode) && e.nodeType === 1;) a = e;
            d.push(a)
        }

        var k = /(?:^|\s)nocode(?:\s|$)/, t = /\r\n?|\n/, s = a.ownerDocument, l;
        a.currentStyle ? l = a.currentStyle.whiteSpace : window.getComputedStyle && (l = s.defaultView.getComputedStyle(a, q).getPropertyValue("white-space"));
        var p = l && "pre" === l.substring(0, 3);
        for (l = s.createElement("LI"); a.firstChild;) l.appendChild(a.firstChild);
        for (var d = [l], g = 0; g < d.length; ++g) e(d[g]);
        m === (m | 0) && d[0].setAttribute("value",
            m);
        var r = s.createElement("OL");
        r.className = "linenums";
        for (var n = Math.max(0, m - 1 | 0) || 0, g = 0, z = d.length; g < z; ++g) l = d[g], l.className = "L" + (g + n) % 10, l.firstChild || l.appendChild(s.createTextNode("\xa0")), r.appendChild(l);
        a.appendChild(r)
    }

    function k(a, m) {
        for (var e = m.length; --e >= 0;) {
            var h = m[e];
            A.hasOwnProperty(h) ? window.console && console.warn("cannot override language handler %s", h) : A[h] = a
        }
    }

    function C(a, m) {
        if (!a || !A.hasOwnProperty(a)) a = /^\s*</.test(m) ? "default-markup" : "default-code";
        return A[a]
    }

    function E(a) {
        var m =
            a.g;
        try {
            var e = M(a.h), h = e.a;
            a.a = h;
            a.c = e.c;
            a.d = 0;
            C(m, h)(a);
            var k = /\bMSIE\b/.test(navigator.userAgent), m = /\n/g, t = a.a, s = t.length, e = 0, l = a.c,
                p = l.length, h = 0, d = a.e, g = d.length, a = 0;
            d[g] = s;
            var r, n;
            for (n = r = 0; n < g;) d[n] !== d[n + 2] ? (d[r++] = d[n++], d[r++] = d[n++]) : n += 2;
            g = r;
            for (n = r = 0; n < g;) {
                for (var z = d[n], f = d[n + 1], b = n + 2; b + 2 <= g && d[b + 1] === f;) b += 2;
                d[r++] = z;
                d[r++] = f;
                n = b
            }
            for (d.length = r; h < p;) {
                var o = l[h + 2] || s, c = d[a + 2] || s, b = Math.min(o, c), i = l[h + 1], j;
                if (i.nodeType !== 1 && (j = t.substring(e, b))) {
                    k && (j = j.replace(m, "\r"));
                    i.nodeValue =
                        j;
                    var u = i.ownerDocument, v = u.createElement("SPAN");
                    v.className = d[a + 1];
                    var x = i.parentNode;
                    x.replaceChild(v, i);
                    v.appendChild(i);
                    e < o && (l[h + 1] = i = u.createTextNode(t.substring(b, o)), x.insertBefore(i, v.nextSibling))
                }
                e = b;
                e >= o && (h += 2);
                e >= c && (a += 2)
            }
        } catch (w) {
            "console" in window && console.log(w && w.stack ? w.stack : w)
        }
    }

    var v = ["break,continue,do,else,for,if,return,while"],
        w = [[v, "auto,case,char,const,default,double,enum,extern,float,goto,int,long,register,short,signed,sizeof,static,struct,switch,typedef,union,unsigned,void,volatile"],
            "catch,class,delete,false,import,new,operator,private,protected,public,this,throw,true,try,typeof"],
        F = [w, "alignof,align_union,asm,axiom,bool,concept,concept_map,const_cast,constexpr,decltype,dynamic_cast,explicit,export,friend,inline,late_check,mutable,namespace,nullptr,reinterpret_cast,static_assert,static_cast,template,typeid,typename,using,virtual,where"],
        G = [w, "abstract,boolean,byte,extends,final,finally,implements,import,instanceof,null,native,package,strictfp,super,synchronized,throws,transient"],
        H = [G, "as,base,by,checked,decimal,delegate,descending,dynamic,event,fixed,foreach,from,group,implicit,in,interface,internal,into,is,lock,object,out,override,orderby,params,partial,readonly,ref,sbyte,sealed,stackalloc,string,select,uint,ulong,unchecked,unsafe,ushort,var"],
        w = [w, "debugger,eval,export,function,get,null,set,undefined,var,with,Infinity,NaN"],
        I = [v, "and,as,assert,class,def,del,elif,except,exec,finally,from,global,import,in,is,lambda,nonlocal,not,or,pass,print,raise,try,with,yield,False,True,None"],
        J = [v, "alias,and,begin,case,class,def,defined,elsif,end,ensure,false,in,module,next,nil,not,or,redo,rescue,retry,self,super,then,true,undef,unless,until,when,yield,BEGIN,END"],
        v = [v, "case,done,elif,esac,eval,fi,function,in,local,set,then,until"],
        K = /^(DIR|FILE|vector|(de|priority_)?queue|list|stack|(const_)?iterator|(multi)?(set|map)|bitset|u?(int|float)\d*)/,
        N = /\S/, O = u({
            keywords: [F, H, w, "caller,delete,die,do,dump,elsif,eval,exit,foreach,for,goto,if,import,last,local,my,next,no,our,print,package,redo,require,sub,undef,unless,until,use,wantarray,while,BEGIN,END" +
            I, J, v], hashComments: !0, cStyleComments: !0, multiLineStrings: !0, regexLiterals: !0
        }), A = {};
    k(O, ["default-code"]);
    k(x([], [["pln", /^[^<?]+/], ["dec", /^<!\w[^>]*(?:>|$)/], ["com", /^<\!--[\S\s]*?(?:--\>|$)/], ["lang-", /^<\?([\S\s]+?)(?:\?>|$)/], ["lang-", /^<%([\S\s]+?)(?:%>|$)/], ["pun", /^(?:<[%?]|[%?]>)/], ["lang-", /^<xmp\b[^>]*>([\S\s]+?)<\/xmp\b[^>]*>/i], ["lang-js", /^<script\b[^>]*>([\S\s]*?)(<\/script\b[^>]*>)/i], ["lang-css", /^<style\b[^>]*>([\S\s]*?)(<\/style\b[^>]*>)/i], ["lang-in.tag", /^(<\/?[a-z][^<>]*>)/i]]),
        ["default-markup", "htm", "html", "mxml", "xhtml", "xml", "xsl"]);
    k(x([["pln", /^\s+/, q, " \t\r\n"], ["atv", /^(?:"[^"]*"?|'[^']*'?)/, q, "\"'"]], [["tag", /^^<\/?[a-z](?:[\w-.:]*\w)?|\/?>$/i], ["atn", /^(?!style[\s=]|on)[a-z](?:[\w:-]*\w)?/i], ["lang-uq.val", /^=\s*([^\s"'>]*(?:[^\s"'/>]|\/(?=\s)))/], ["pun", /^[/<->]+/], ["lang-js", /^on\w+\s*=\s*"([^"]+)"/i], ["lang-js", /^on\w+\s*=\s*'([^']+)'/i], ["lang-js", /^on\w+\s*=\s*([^\s"'>]+)/i], ["lang-css", /^style\s*=\s*"([^"]+)"/i], ["lang-css", /^style\s*=\s*'([^']+)'/i], ["lang-css",
        /^style\s*=\s*([^\s"'>]+)/i]]), ["in.tag"]);
    k(x([], [["atv", /^[\S\s]+/]]), ["uq.val"]);
    k(u({keywords: F, hashComments: !0, cStyleComments: !0, types: K}), ["c", "cc", "cpp", "cxx", "cyc", "m"]);
    k(u({keywords: "null,true,false"}), ["json"]);
    k(u({keywords: H, hashComments: !0, cStyleComments: !0, verbatimStrings: !0, types: K}), ["cs"]);
    k(u({keywords: G, cStyleComments: !0}), ["java"]);
    k(u({keywords: v, hashComments: !0, multiLineStrings: !0}), ["bsh", "csh", "sh"]);
    k(u({keywords: I, hashComments: !0, multiLineStrings: !0, tripleQuotedStrings: !0}),
        ["cv", "py"]);
    k(u({
        keywords: "caller,delete,die,do,dump,elsif,eval,exit,foreach,for,goto,if,import,last,local,my,next,no,our,print,package,redo,require,sub,undef,unless,until,use,wantarray,while,BEGIN,END",
        hashComments: !0,
        multiLineStrings: !0,
        regexLiterals: !0
    }), ["perl", "pl", "pm"]);
    k(u({keywords: J, hashComments: !0, multiLineStrings: !0, regexLiterals: !0}), ["rb"]);
    k(u({keywords: w, cStyleComments: !0, regexLiterals: !0}), ["js"]);
    k(u({
        keywords: "all,and,by,catch,class,else,extends,false,finally,for,if,in,is,isnt,loop,new,no,not,null,of,off,on,or,return,super,then,true,try,unless,until,when,while,yes",
        hashComments: 3, cStyleComments: !0, multilineStrings: !0, tripleQuotedStrings: !0, regexLiterals: !0
    }), ["coffee"]);
    k(x([], [["str", /^[\S\s]+/]]), ["regex"]);
    window.prettyPrintOne = function (a, m, e) {
        var h = document.createElement("PRE");
        h.innerHTML = a;
        e && D(h, e);
        E({g: m, i: e, h: h});
        return h.innerHTML
    };
    window.prettyPrint = function (a) {
        function m() {
            for (var e = window.PR_SHOULD_USE_CONTINUATION ? l.now() + 250 : Infinity; p < h.length && l.now() < e; p++) {
                var n = h[p], k = n.className;
                if (k.indexOf("prettyprint") >= 0) {
                    var k = k.match(g), f, b;
                    if (b =
                        !k) {
                        b = n;
                        for (var o = void 0, c = b.firstChild; c; c = c.nextSibling) var i = c.nodeType, o = i === 1 ? o ? b : c : i === 3 ? N.test(c.nodeValue) ? b : o : o;
                        b = (f = o === b ? void 0 : o) && "CODE" === f.tagName
                    }
                    b && (k = f.className.match(g));
                    k && (k = k[1]);
                    b = !1;
                    for (o = n.parentNode; o; o = o.parentNode) if ((o.tagName === "pre" || o.tagName === "code" || o.tagName === "xmp") && o.className && o.className.indexOf("prettyprint") >= 0) {
                        b = !0;
                        break
                    }
                    b || ((b = (b = n.className.match(/\blinenums\b(?::(\d+))?/)) ? b[1] && b[1].length ? +b[1] : !0 : !1) && D(n, b), d = {
                        g: k,
                        h: n,
                        i: b
                    }, E(d))
                }
            }
            p < h.length ? setTimeout(m,
                250) : a && a()
        }

        for (var e = [document.getElementsByTagName("pre"), document.getElementsByTagName("code"), document.getElementsByTagName("xmp")], h = [], k = 0; k < e.length; ++k) for (var t = 0, s = e[k].length; t < s; ++t) h.push(e[k][t]);
        var e = q, l = Date;
        l.now || (l = {
            now: function () {
                return +new Date
            }
        });
        var p = 0, d, g = /\blang(?:uage)?-([\w.]+)(?!\S)/;
        m()
    };
    window.PR = {
        createSimpleLexer: x,
        registerLangHandler: k,
        sourceDecorator: u,
        PR_ATTRIB_NAME: "atn",
        PR_ATTRIB_VALUE: "atv",
        PR_COMMENT: "com",
        PR_DECLARATION: "dec",
        PR_KEYWORD: "kwd",
        PR_LITERAL: "lit",
        PR_NOCODE: "nocode",
        PR_PLAIN: "pln",
        PR_PUNCTUATION: "pun",
        PR_SOURCE: "src",
        PR_STRING: "str",
        PR_TAG: "tag",
        PR_TYPE: "typ"
    }
})();