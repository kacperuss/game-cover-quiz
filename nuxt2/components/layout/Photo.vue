<template>
    <picture class="block">
        <source :srcset="src_dsk" media="(min-width: 768px)" />
        <img
            :src="src_mob || src_dsk"
            class="w-full h-full"
            :class="{ 'object-contain': contain, 'object-cover': !contain }"
        />
    </picture>
</template>

<script>
export default {
    props: ['src_dsk', 'src_mob', 'contain'],
}
</script>

<style lang="scss"></style>
