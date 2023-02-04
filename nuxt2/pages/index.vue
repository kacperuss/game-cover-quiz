<template>
    <main class="flex flex-col h-screen">
        <ChooseDiff v-if="!diff_chosen" class="flex-1" id="choose_diff" />
        <Header v-if="diff_chosen" :diff="difficulty" />
        <MainGuess
            v-if="diff_chosen"
            class="flex-1"
            id="main_guess"
            :loading="loading"
            :image="loading ? null : image"
            :names="names"
        />
        <Footer />
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
        difficulty: {
            name: 'Auto',
            number: 200,
        },
        diff_chosen: false,
    }),
    methods: {
        set_diff(new_diff) {
            this.difficulty = new_diff
            this.diff_chosen = true
            if (!this.loading) this.set_random_game()
            localStorage.removeItem('prev_games')
        },
        open_choose_diff() {
            localStorage.removeItem('difficulty')
            this.diff_chosen = false
        },

        get_rand_num() {
            // Higher changes of lower index = more popular games
            let epic_random_number = Math.random()
            // return epic_random_number * epic_random_number
            return epic_random_number
        },

        async fetch_api() {
            let json_data = await (await fetch('/api.json')).json()
            this.api_data = json_data
            // console.log(json_data)
            this.loading = false
        },
        async set_random_game() {
            const s_key = this.api_data[0].names ? 'screenshots' : 's'
            const n_key = this.api_data[0].names ? 'names' : 'n'
            const f_key = this.api_data[0].names ? 'franchises' : 'f'

            let prev_games =
                (() => {
                    if (!localStorage['prev_games']) return
                    try {
                        return JSON.parse(localStorage['prev_games'])
                    } catch {
                        console.log('Invalid prev_games in local storage')
                        localStorage.removeItem('prev_games')
                        return
                    }
                })() || []

            const max_index = Math.min(this.difficulty.number, this.api_data.length)
            const max_history_len = Math.floor(max_index / 10)

            let i = -1
            let tries = 20
            while (tries > 0 && (i == -1 || prev_games.includes(i))) {
                i = parseInt(this.get_rand_num() * max_index)
                tries -= 1
            }

            if (prev_games.length >= max_history_len) prev_games = prev_games.slice(1)
            prev_games = prev_games.concat([i])
            localStorage['prev_games'] = JSON.stringify(prev_games)

            const j = parseInt(Math.random() * this.api_data[i][s_key].length)
            const ss = this.api_data[i][s_key][j]
            this.image = `${BASE_URL}${ss}.png`
            this.names = this.api_data[i][n_key]
            this.loading = false
            setTimeout(() => {
                if (document.querySelector('#answer_form input')) document.querySelector('#answer_form input').focus()
            }, 200)
        },
        async init() {
            await this.fetch_api()
            if (this.diff_chosen) await this.set_random_game()
        },
    },
    mounted() {
        this.init()
    },
}
</script>

<style lang="scss" scoped></style>
