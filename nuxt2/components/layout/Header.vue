<template>
    <section class="text-6 py-4 px-32 flex justify-between items-center bg-black text-white gap-4">
        <div class="underline cursor-pointer _a" @click="on_change_diff">Change difficulty</div>
        <div class="">
            <div v-if="diff" class="">Current difficulty: {{ diff['name'] }} ({{ diff['number'] }})</div>
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
