<template>
  <div>
    <h3 class="text-lg font-semibold mb-4">{{ title }}</h3>
    <ul class="space-y-2">
      <li v-for="link in links" :key="link.text">
        <a :href="link.href" class="text-gray-400 hover:text-white">{{ link.text }}</a>
      </li>
    </ul>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  links: Array
})
</script>