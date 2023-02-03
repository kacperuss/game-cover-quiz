import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/dist/ScrollTrigger.min'

gsap.registerPlugin(ScrollTrigger)

export default (context, inject) => {
    const img = (img_obj, desktop = true, size = null) => {
        if (!img_obj || img_obj.image === undefined || img_obj.imagemob === undefined) {
            return ''
        }
        let _img = desktop || !img_obj.imagemob ? img_obj.image : img_obj.imagemob
        if (_img.sizes && size) {
            return _img.sizes[size] ? _img.sizes[size] : ''
        }
        return _img.url ? _img.url : ''
    }
    inject('img', img)
    context.$img = img

    const fadeUpInit = () => {
        gsap.utils.toArray('.fadeUp').forEach((elem) => {
            let _delay = elem.getAttribute('fadeUpDelay')
            let _fire_soon = elem.getAttribute('fadeUpFireSoon')
            gsap.fromTo(
                elem,
                { y: `${100 / 16}rem`, opacity: 0 },
                {
                    y: 0,
                    opacity: 1,

                    duration: 1,
                    delay: _delay ? _delay : 0,
                    paused: true,
                    ease: 'sine.out',

                    scrollTrigger: {
                        trigger: elem,
                        start: _fire_soon ? '-=100 bottom' : '-=100 80%',
                        end: _fire_soon ? '-=100 bottom' : '-=100 80%',
                    },
                }
            )
        })
        ScrollTrigger.refresh()
    }
    inject('fadeUpInit', fadeUpInit)
    context.$fadeUpInit = fadeUpInit

    const getRootVar = (varName) => {
        return getComputedStyle(document.documentElement).getPropertyValue(varName)
    }
    inject('getRootVar', getRootVar)
    context.$getRootVar = getRootVar

    const toggleBodyScroll = (force = null) => {
        if (force === null) {
            document.documentElement.classList.toggle('overflow-hidden')
            document.body.classList.toggle('overflow-hidden')
        }
        if (force === true) {
            document.documentElement.classList.add('overflow-hidden')
            document.body.classList.add('overflow-hidden')
        }
        if (force === false) {
            document.documentElement.classList.remove('overflow-hidden')
            document.body.classList.remove('overflow-hidden')
        }
    }
    inject('toggleBodyScroll', toggleBodyScroll)
    context.$toggleBodyScroll = toggleBodyScroll
}
