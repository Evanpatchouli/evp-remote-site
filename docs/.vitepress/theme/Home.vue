<script setup>
import OrbitHero from './OrbitHero.vue'
</script>

<template>
  <div class="product-home">
    <OrbitHero />
    <div class="guide-surface"><section class="paths" aria-labelledby="choose-title">
      <p class="kicker">FIELD GUIDE <span>/</span> 使用手册</p><h2 id="choose-title">你想连接哪台电脑？</h2>
      <div class="path-grid">
        <a class="path" href="/guide/share.html"><span class="path-id">01 / ASSIST</span><h3>亲友的电脑 <span aria-hidden="true">↗</span></h3><p>让对方创建邀请码。默认需要本人同意，才会共享桌面。</p></a>
        <a class="path" href="/guide/pair.html"><span class="path-id">02 / DEVICES</span><h3>自己的电脑 <span aria-hidden="true">↗</span></h3><p>两台电脑配对一次。允许远控后，下次从设备列表连接。</p></a>
      </div>
    </section></div>
  </div>
</template>
