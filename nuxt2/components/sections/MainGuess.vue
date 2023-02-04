<template>
    <section class="relative">
        <div id="bg-img" class="absolute w-full h-full left-0 top-0">
            <img v-if="image" :src="image" class="block w-full h-full" />
        </div>
        <div class="px-32 py-8 relative h-full w-full flex justify-center items-center flex-col gap-8">
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
                <button class="_skip" @click="show_answer()">Show answer</button>
                <!-- <button class="_skip" @click="show_answer()">Give up</button> -->
                <!-- <input v-if="loading" type="disabled" disabled="disabled" /> -->
                <!-- <input v-else type="text" @keypress="on_key_input" /> -->
                <!-- <button class="_enter" @click="check_answer()">Enter</button> -->
            </div>
            <div id="answer_result" v-if="answered" class="">
                <div class="w-25"></div>
                <div class="_game_name">{{ names[0] }}</div>
                <button class="_next" @click="load_next()">Next</button>
            </div>
            <div class="">
                <button class="_report w-70" @click="show_report()">Mark / report the screenshot</button>
            </div>
        </div>
    </section>
</template>

<script>
export default {
    data: () => ({
        answered: false,
    }),
    props: ['image', 'names', 'loading'],
    methods: {
        show_answer() {
            if (this.loading) return
            this.answered = true
        },
        on_key_input(e) {
            if (this.loading) return
            if (e.key == 'Enter') {
                e.preventDefault()
                this.check_answer()
            }
        },
        load_next() {
            if (this.loading) return
            this.answered = false
            this.$parent.loading = true
            setTimeout(() => {
                this.$parent.set_random_game()
            }, 50)
        },
        check_answer() {
            if (this.loading) return
            console.log('check')
        },
        show_report() {
            console.log('report')
        },

        on_keypress_body(e) {
            const input = document.querySelector('#answer_form input')
            if (!input) return
            if (e.target == input) return
            input.focus()
            if (e.key.length == 1) {
                input.value = input.value + e.key
            }
        },
    },
    beforeMount() {
        document.removeEventListener('keypress', this.on_keypress_body)
    },
    beforeDestroy() {
        document.removeEventListener('keypress', this.on_keypress_body)
    },
    mounted() {
        document.addEventListener('keypress', this.on_keypress_body)
    },
}
</script>

<style lang="scss" scoped>
#main_img {
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
    }
    ._next {
        background: rgb(46, 117, 28);
    }
}
</style>
