<template>
  <footer class="bg-gray-900 text-white py-12">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-8">
        <FooterSection
          v-for="section in sections"
          :key="section.title"
          v-bind="section"
        />
      </div>
      <div class="mt-8 pt-8 border-t border-gray-800 text-center text-gray-400">
        <p>&copy; {{ new Date().getFullYear() }} TextMarley. All rights reserved.</p>
      </div>
    </div>
  </footer>
</template>

<script setup>
import FooterSection from './FooterSection.vue'

const sections = [
  {
    title: 'Product',
    links: [
      { text: 'Features', href: '#features' },
      { text: 'Pricing', href: '#pricing' },
      { text: 'Security', href: '#' }
    ]
  },
  {
    title: 'Company',
    links: [
      { text: 'About', href: '#' },
      { text: 'Careers', href: '#' },
      { text: 'Contact', href: '#contact' }
    ]
  },
  {
    title: 'Resources',
    links: [
      { text: 'Blog', href: '#' },
      { text: 'Documentation', href: '#' },
      { text: 'Help Center', href: '#' }
    ]
  },
  {
    title: 'Legal',
    links: [
      { text: 'Privacy', href: '#' },
      { text: 'Terms', href: '#' },
      { text: 'Security', href: '#' }
    ]
  }
]
</script>