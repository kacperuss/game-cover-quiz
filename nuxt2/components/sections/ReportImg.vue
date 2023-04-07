<template>
    <section class="">
        <div class="" v-if="!answered">
            <div class="text-12 uppercase pb-6">Mark / report the screenshot</div>
            <div class="text-8 pb-12">Please choose an option that describes the issue the most:</div>
            <div class="options flex flex-col gap-3 leading-14">
                <button class="" v-for="(r, i) in reasons" :key="i" @click="send_report(i)">
                    {{ r }}
                </button>
            </div>
        </div>
        <div class="" v-if="answered">
            <div class="text-12 uppercase pb-6">Thank you for your cooperation</div>
            <button class="" @click="close">Go back</button>
        </div>
    </section>
</template>

<script>
import md5 from 'md5'

export default {
    props: ['image', 'game'],
    data: () => ({
        answered: false,
        reasons: {
            logo: 'The screenshot contains a game logo / name',
            no_info: 'The screenshot is insufficient to determine the game',
            wrong_game: 'The screenshot is not from this game',
            bad_img: 'The image is not a video game screenshot',
            porn: 'The image is obscene or inappropriate',
            dead_url: 'The image is not loading',
            bitching: 'The game should not be present in the quiz',
            other: 'Other issue',
        },
    }),
    methods: {
        async sendPOST(url = '', data = {}) {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            })
            console.log(await response.json())
        },
        get_token() {
            let x = Math.floor(Math.random() * 4185324489642323)
            let hash = md5(`${x}`)
            let secret = md5(hash.substring(16) + hash.substring(0, 16)) + md5(md5(hash))
            console.log(x, hash, secret)

            return { id: x, token: secret }
        },
        async send_report(rep) {
            let token = this.get_token()
            token['report'] = rep
            token['image'] = this.image
            token['game'] = this.game
            await this.sendPOST(`/get_reports.php`, token)
            this.answered = true
        },
        close() {
            this.$parent.hide_report()
        },
    },
}
</script>

<style lang="scss" scoped>
section {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    z-index: 100;
    background: #222e;

    & > div {
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
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
}
</style>
