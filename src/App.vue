<script setup lang="ts">
// https://github.com/vueuse/head
// you can use this to manipulate the document head in any components,
// they will be rendered correctly in the html results with vite-ssg
useHead({
  title: 'CloudApp',
  meta: [
    { name: 'description', content: 'Modern Stack Cloud Based API' },
    {
      name: 'theme-color',
      content: computed(() => isDark.value ? '#00aba9' : '#ffffff'),
    },
  ],
  link: [
    {
      rel: 'icon',
      type: 'image/svg+xml',
      href: computed(() => preferredDark.value ? '/favicon.svg' : '/logo.svg'),
    },
  ],
})
const route = useRoute()
const cls = ref((route.path.startsWith('/blog')) ? 'blog' : 'home')


</script>

<template>
<section :class="cls">
<Logo/>
  <RouterView />
  </section>

</template>


<style global>
.blog {
  background-image: url('/bg.jpg');
  background-size: cover;
  background-position: fixed;
  background-repeat: no-repeat;
}

.blog_dark {
  background-image: url('/bg_dark.jpg');
  background-size: cover;
  background-position: fixed;
  background-repeat: no-repeat;
}

</style>
