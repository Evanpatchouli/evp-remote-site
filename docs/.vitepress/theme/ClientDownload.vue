<script setup>
const value = import.meta.env.VITE_CLIENT_DOWNLOAD_URL?.trim()
const url = URL.canParse(value) && ['http:', 'https:'].includes(new URL(value).protocol) ? value : ''
</script>

<template>
  <a v-if="url" :href="url" class="download-action"><svg aria-hidden="true" width="17" height="17" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M10 2v10m-4-4 4 4 4-4M3 13v4h14v-4"/></svg>下载 Windows 客户端</a>
  <span v-else class="download-missing">下载地址尚未配置</span>
</template>
