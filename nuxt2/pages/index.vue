<template>
    <main class="grid grid-cols-1">
        <MainGuess id="main_guess" :loading="loading" :image="loading ? null : image" :names="names" />
        <div class="h-12 flex justify-center items-center bg-indigo-900 text-white gap-4">
            <div class="">
                Written by <a target="_blank" class="underline" href="https://kacperuss.pl/">Kacperuss</a>
            </div>
            <div class="">-</div>
            <div class="">Built with <a target="_blank" class="underline" href="https://nuxtjs.org/">Nuxt</a></div>
            <div class="">-</div>
            <div class="">Powered by <a target="_blank" class="underline" href="https://www.igdb.com/">IGDB</a></div>
            <div class="">-</div>
            <div class="">
                Source on
                <a target="_blank" class="underline" href="https://github.com/kacperuss/game-cover-quiz">GitHub</a>
            </div>
        </div>
    </main>
</template>

<script>
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/dist/ScrollTrigger.min'

gsap.registerPlugin(ScrollTrigger)

const BASE_URL = 'https://images.igdb.com/igdb/image/upload/t_1080p/'

export default {
    data: () => ({
        api_data: [],
        loading: true,
        image: null,
        names: [],
    }),
    methods: {
        async fetch_api() {
            let json_data = await (await fetch('/api.json')).json()
            this.api_data = json_data
            // console.log(json_data)
        },
        async set_random_game() {
            const i = parseInt(Math.random() * this.api_data.length)
            const j = parseInt(Math.random() * this.api_data[i].screenshots.length)
            const ss = this.api_data[i].screenshots[j]
            this.image = `${BASE_URL}${ss}.png`
            this.names = this.api_data[i].names
            this.loading = false
            setTimeout(() => {
                document.querySelector('#answer_form input').focus()
            }, 200)
        },
    },
    async mounted() {
        await this.fetch_api()
        await this.set_random_game()
    },
}
</script>

<style lang="scss" scoped>
#main_guess {
    height: calc(100dvh - 12rem / 4);
}
</style>
