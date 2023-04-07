<template>
    <section class="relative">
        <div id="bg-img" class="absolute w-full h-full left-0 top-0">
            <img v-if="image" :src="image" class="block w-full h-full" />
        </div>
        <div class="px-32 py-8 relative h-full w-full flex justify-center items-center flex-col gap-4">
            <div id="main_img" class="w-full h-10 flex-1 relative">
                <video
                    :src="require('~/assets/vid/loading2_indigo.mp4')"
                    class="block w-full h-full absolute left-0 top-0"
                    loop
                    autoplay
                    muted
                ></video>
                <img v-if="image" :src="image" class="block w-full h-full absolute top-0 left-0" />
            </div>
            <div id="answer_form" v-if="!answered">
                <!-- <button class="_skip" @click="show_answer()">Show answer</button> -->
                <button class="_skip" @click="show_answer()">
                    Give up
                    <div class="__smol">(ESC)</div>
                </button>
                <input v-if="loading" type="disabled" disabled="disabled" />
                <input
                    v-else
                    type="text"
                    @keypress="on_key_input"
                    @input="on_input_change"
                    :class="wrong ? '__wrong' : ''"
                />
                <button class="_enter" @click="check_answer()">
                    Enter
                    <div class="__smol">(Enter)</div>
                </button>
            </div>
            <div id="answer_result" v-if="answered" class="">
                <div class="w-25"></div>
                <div class="_game_name" :class="correct ? 'correct' : 'skipped'">{{ names[0] }}</div>
                <button class="_next" @click="load_next()">
                    Next
                    <div class="__smol">(Enter)</div>
                </button>
            </div>
            <div class="" v-if="answered">
                <button class="_report w-70" @click="show_report()">Mark / report the screenshot</button>
            </div>
        </div>
    </section>
</template>

<script>
import levenshtein from 'js-levenshtein'

const $ = (x) => document.querySelector(x)
const $$ = (x) => document.querySelectorAll(x)

export default {
    data: () => ({
        answered: false,
        correct: false,
        can_go_next: false,
        wrong: false,
    }),
    props: ['image', 'names', 'loading', 'reporting'],
    methods: {
        show_answer(correct = false) {
            if (this.loading || this.reporting) return
            this.correct = correct
            this.answered = true
            setTimeout(() => {
                this.can_go_next = true
            }, 50)
        },
        on_input_change(e) {
            this.wrong = false
        },
        on_key_input(e) {
            if (this.loading || this.reporting) return
            if (e.key == 'Enter') {
                e.preventDefault()
                this.check_answer()
            }
        },
        load_next() {
            if (this.loading || this.reporting) return
            this.answered = false
            this.correct = false
            this.can_go_next = false
            this.wrong = false
            this.$parent.loading = true
            setTimeout(() => {
                this.$parent.set_random_game()
            }, 50)
        },
        normalise_name(name) {
            return name
                .split(':')[0]
                .toLowerCase()
                .replaceAll(/[^a-z]/g, '')
                .replaceAll('the', '')
        },
        check_answer() {
            if (this.loading || this.reporting) return
            // console.log('check')
            const input = $('#answer_form input')
            if (!input || !input.value) return
            let guess = input.value.toLowerCase()
            let norm_guess = this.normalise_name(guess) || guess
            for (let i = 0; i < this.names.length; ++i) {
                let x = this.names[i].toLowerCase()

                if (x.length > 6 && x.search(guess) != -1 && x.length < guess.length * 2) return this.show_answer(true)

                let xx = this.normalise_name(x) || x
                let err = Math.min(levenshtein(x, guess) / x.length, levenshtein(xx, norm_guess) / xx.length)
                if (err < 0.26) return this.show_answer(true)
            }

            this.wrong = true
        },
        show_report() {
            if (this.loading || this.reporting) return
            this.$parent.show_report()
        },

        on_keypress_body(e) {
            const input = $('#answer_form input')
            if (input && !this.answered && e.key == 'Escape') return this.show_answer()
            if (!input && this.answered && this.can_go_next && e.key == 'Enter') return this.load_next()
            if (!input) return
            if (e.target == input) return
            input.focus()
            if (e.key.length == 1) {
                // input.value = input.value + e.key
            }
        },
    },
    beforeMount() {
        document.removeEventListener('keydown', this.on_keypress_body)
    },
    beforeDestroy() {
        document.removeEventListener('keydown', this.on_keypress_body)
    },
    mounted() {
        document.addEventListener('keydown', this.on_keypress_body)
    },
}
</script>

<style lang="scss" scoped>
#main_img {
    min-height: calc(100vh - 300rem / 16);
    img {
        filter: drop-shadow(0 0 20px #000);
        object-fit: contain;
    }
    video {
        width: auto;
        left: 50%;
        transform: translateX(-50%);
        aspect-ratio: 1;
        object-fit: cover;
    }
}
#bg-img {
    filter: blur(30px);
    opacity: 0.1;
    img {
        object-fit: cover;
    }
}
button {
    display: block;
    min-width: calc(100rem / 16);
    background: #4c718a;
    box-shadow: 0 0 4px #000;
    padding: 8px 16px;
    transition: opacity 0.3s;
    &:hover {
        opacity: 0.6;
    }
    &:active {
        opacity: 0.3;
    }
    .__smol {
        font-size: 0.8em;
        opacity: 0.5;
    }
}
#answer_form {
    display: flex;
    gap: calc(20rem / 16);
    align-items: center;
    input {
        display: block;
        background: #fff2;
        border: none;
        box-shadow: 0 0 4px #000;
        padding: calc(4rem / 16) calc(8rem / 16);
        font-size: calc(20rem / 16);
        width: calc(400rem / 16);
        text-align: center;
        outline: none;
        border: 1px solid transparent;
        &.__wrong {
            border-color: #912b23;
            background: #2b2120;
        }
        &:not(.__wrong) {
            &:active,
            &:focus,
            &:focus-visible {
                border-color: #4089b9;
            }
        }
    }
    button._skip {
        background: rgb(129, 112, 37);
    }
    button._enter {
        background: rgb(46, 117, 28);
    }
}
#answer_result {
    display: flex;
    gap: calc(20rem / 16);
    align-items: center;
    ._game_name {
        font-size: calc(32rem / 16);
        line-height: 1;
        &.correct {
            color: rgb(98, 173, 79);
        }
        &.skipped {
            color: rgb(216, 190, 77);
        }
    }
    ._next {
        background: rgb(46, 117, 28);
    }
}
</style>
