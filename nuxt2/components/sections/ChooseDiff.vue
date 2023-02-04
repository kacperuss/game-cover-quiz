<template>
    <section class="flex flex-col gap-4 justify-center items-center">
        <img
            :src="require('~/assets/img/SplashMGS5.png')"
            class="w-300 h-40 max-h-[12vh] object-contain"
            alt="Game Cover"
        />
        <div class="pt-16 text-10">Choose your difficulty</div>
        <div class="pt-4 flex gap-8">
            <button
                :class="i == current ? '_active' : ''"
                v-for="(d, i) in diffs"
                :key="`btn_${i}`"
                @click="on_btn_click(i)"
            >
                {{ d.name }}
            </button>
        </div>
        <div class="__cur_diff pt-4 w-120">
            <div class="flex justify-between text-6 h-[1em]">
                <div class="">{{ current == -1 ? '' : diffs[current]['name'] }}</div>
                <div v-if="current != -1" class="">{{ diffs[current]['number'] }} Games</div>
            </div>
            <div class="__desc h-48 --font-secondary pt-6 text-center">
                <div v-if="current != -1" v-html="diffs[current]['desc']"></div>
            </div>
            <div class="pt-8">
                <button
                    class="w-60 mx-auto _green"
                    :disabled="current == -1 ? 'disabled' : null"
                    @click="on_play_click()"
                >
                    Play
                </button>
            </div>
        </div>
    </section>
</template>

<script>
export default {
    data: () => ({
        current: -1,
        diffs: [
            {
                name: 'Casual',
                number: 200,
                desc: `A simple list of most popular video games.<br/><br/>
                    Many of them are well-known franchises with movie and book tie-ins, which makes them
                    easy to guess. This list will test any non-gamers, but most of those who regularly
                    enjoy video games should not have much trouble recognising any of them.<br/><br/>
                    Intended for those who play casually or not at all.`,
            },
            {
                name: 'Advanced',
                number: 1500,
                desc: `Much wider list with some obscure titles.<br/><br/>
                    The difficulty gets higher. This list, while still containing all games from 'Casual',
                    requires mush richer video game knowledge. A mix of big franchises, less popular
                    titles and hidden gems.<br/><br/>
                    Intended for average video game enjoyers.`,
            },
            {
                name: 'Full',
                number: 5000,
                desc: `Most challenging of the lists.<br/><br/>
                    Containing all the games from our database, this list poses a real challenge.
                    From <nw>pre-retro</nw> classics to forgotten indies, mastering this difficulty
                    requires <nw>a near-perfect</nw> knowledge spanning half a century of video game
                    history.<br/><br/>
                    Intended for gaming scholars with decades of experience.`,
            },
        ],
    }),
    methods: {
        on_btn_click(i) {
            this.current = i
        },
        on_play_click() {
            if (this.current == -1) return
            this.$parent.set_diff({
                name: this.diffs[this.current]['name'],
                number: this.diffs[this.current]['number'],
            })
            localStorage['difficulty'] = this.current
        },
    },

    mounted() {
        if (localStorage['difficulty']) {
            try {
                const d = parseInt(localStorage['difficulty'])
                if (d >= 0 && d < this.diffs.length) {
                    this.on_btn_click(d)
                    this.on_play_click()
                }
            } catch {
                console.log('Invalid diff in local storage')
                localStorage.removeItem('difficulty')
            }
        }
    },
}
</script>

<style lang="scss" scoped>
.__desc::v-deep nw {
    white-space: nowrap;
}
button {
    display: block;
    min-width: calc(100rem / 16);
    background: #4c718a;
    box-shadow: 0 0 4px #000;
    padding: 8px 16px;
    transition: opacity 0.3s, background-color 0.2s, color 0.2s;
    &:hover {
        opacity: 0.6;
    }
    &:active {
        opacity: 0.3;
    }
    &._active {
        background: rgb(147, 212, 255);
        color: black;
    }
    &._disabled,
    &:disabled {
        opacity: 0.2;
        cursor: default;
    }
    &._green {
        background: rgb(46, 117, 28);
    }
}
@media (min-aspect-ratio: 2.6) and (max-width: 1920px) {
    .__desc {
        display: none;
    }
    .__cur_diff {
        width: max-content;
    }
}
@media (max-height: 760px) and (min-width: 1920px) {
    .__desc {
        display: none;
    }
    .__cur_diff {
        width: max-content;
    }
}
</style>
