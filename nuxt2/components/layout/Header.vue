<template>
    <section class="text-4 md:text-6 p-5 md:py-4 md:px-32 flex justify-between items-center bg-black text-white gap-4">
        <div class="underline cursor-pointer _a" @click="on_change_diff">Change difficulty</div>
        <div class="flex flex-col items-end md:gap-4 md:flex-row">
            <div v-if="diff" class="">Current difficulty:</div>
            <div v-if="diff" class="">{{ diff['name'] }} ({{ diff['number'] }})</div>
        </div>
    </section>
</template>

<script>
export default {
    props: ['diff'],
    methods: {
        on_change_diff() {
            this.$parent.open_choose_diff()
        },
    },
}
</script>

<style lang="scss" scoped>
section {
    box-shadow: 0 0 20px black;
}
</style>
