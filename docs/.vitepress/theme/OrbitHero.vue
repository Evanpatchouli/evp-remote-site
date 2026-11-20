<script setup>
import { nextTick, onMounted, onBeforeUnmount, ref } from 'vue'

const stage = ref(null)
const track = ref(null)
const actionSlot = ref(null)
const actions = ref(null)
const floating = ref(false)
const docked = ref(false)
const paused = ref(false)
const reduced = ref(false)
const screens = Array.from({ length: 16 }, (_, index) => ({ phase: index / 16 * Math.PI * 2, crop: (index * 37) % 100 }))
function pose(phase, index, travel = 0) {
  const angle = phase + travel
  const depth = (1 + Math.cos(angle - .65 + index % 3 * .48)) / 2
  const radius = .83 + depth * .19 + (index % 3) * .09
  return {
    left: `${50 + Math.cos(angle) * 45 * radius}%`, top: `${50 + Math.sin(angle) * 44 * radius}%`,
    transform: `translate(-50%, -50%) perspective(450px) rotateY(${22 * Math.sin(angle)}deg) rotateZ(${8 * Math.cos(angle * 2)}deg) scale(${.37 + depth * .7})`,
    opacity: (.32 + depth * .68).toFixed(3), zIndex: Math.round(depth * 7)
  }
}

let cleanup = () => {}
onMounted(() => {
  const motion = matchMedia('(prefers-reduced-motion: reduce)')
  const nodes = Array.from(stage.value.querySelectorAll('.orbit-screen'))
  const logo = stage.value.querySelector('.brand-relief')
  let flight
  let revision = 0
  function alignActions(slot) {
    actions.value.style.setProperty('--slot-center', `${slot.top + slot.height / 2}px`)
  }
  async function moveActions(next) {
    const ticket = ++revision
    const start = floating.value ? getComputedStyle(actions.value).getPropertyValue('--dock-progress').trim() : '0'
    const focus = actions.value.contains(document.activeElement) ? document.activeElement : null
    docked.value = next
    floating.value = true
    await nextTick()
    if (ticket !== revision) return
    focus?.focus({ preventScroll: true })
    alignActions(actionSlot.value.getBoundingClientRect())
    flight?.cancel()
    const end = next ? 1 : 0
    actions.value.style.setProperty('--dock-progress', end)
    if (!motion.matches && !paused.value) {
      flight = actions.value.animate([{ '--dock-progress': start || '0' }, { '--dock-progress': String(end) }], {
        duration: 380 * Math.abs(end - Number(start)), easing: 'cubic-bezier(0.72, 0, 0.28, 1)'
      })
      try { await flight.finished } catch { return }
    }
    if (ticket === revision && !next) {
      const active = actions.value.contains(document.activeElement) ? document.activeElement : null
      floating.value = false
      await nextTick()
      active?.focus({ preventScroll: true })
    }
  }
  function placeActions() {
    const slot = actionSlot.value.getBoundingClientRect()
    const guideTop = track.value.getBoundingClientRect().bottom
    const fadeHeight = parseFloat(getComputedStyle(track.value.nextElementSibling, '::before').height) || 0
    const navHeight = parseFloat(getComputedStyle(stage.value).getPropertyValue('--vp-nav-height')) || 64
    if (floating.value) alignActions(slot)
    const next = slot.bottom >= guideTop - fadeHeight || slot.top < navHeight || slot.bottom > window.innerHeight
    if (next !== docked.value) moveActions(next)
  }
  let placement = 0
  function scheduleActions() {
    if (!placement) placement = requestAnimationFrame(() => { placement = 0; placeActions() })
  }
  let request = 0, previous = 0, idle = 0, progress = 0, visible = true
  function frame(now) {
    request = 0
    if (document.hidden || !visible || reduced.value || paused.value) { previous = 0; return }
    const delta = previous ? Math.min(now - previous, 64) : 0
    previous = now
    idle += delta * .000055
    const bounds = track.value.getBoundingClientRect()
    const leaving = Math.max(0, stage.value.offsetHeight + 64 - bounds.bottom)
    root.style.translate = `0 ${Math.min(leaving * .56, stage.value.offsetHeight * .5)}px`
    if (floating.value && flight?.playState === 'running') alignActions(actionSlot.value.getBoundingClientRect())
    const target = Math.max(0, Math.min(1, (64 - bounds.top) / Math.max(1, bounds.height - stage.value.offsetHeight)))
    progress += (target - progress) * (1 - Math.exp(-delta / 100))
    logo.style.transform = `perspective(850px) rotateX(12deg) rotateY(${-22 + progress * 295 + 5 * Math.sin(idle)}deg) rotateZ(-13deg)`
    const width = root.clientWidth, height = root.clientHeight
    nodes.forEach((node, index) => {
      const phase = screens[index].phase
      const style = pose(phase, index, idle + progress * 1.5)
      const zoom = 1 + .34 * Math.sin(phase + progress * Math.PI * 2) * Math.sin(progress * Math.PI)
      node.style.transform = `translate(${(parseFloat(style.left) - 50) * width / 100 * zoom}px, ${(parseFloat(style.top) - 50) * height / 100 * zoom}px) ${style.transform} scale(${zoom})`
      node.style.opacity = style.opacity
      node.style.zIndex = style.zIndex
    })
    root.classList.add('orbit-ready')
    request = requestAnimationFrame(frame)
  }
  function wake() { if (!request) request = requestAnimationFrame(frame) }
  function preference() { reduced.value = motion.matches; if (motion.matches) root.style.translate = ''; wake() }
  const observer = new IntersectionObserver(([entry]) => { visible = entry.isIntersecting; wake() })
  const root = stage.value
  observer.observe(root)
  const resizeObserver = new ResizeObserver(scheduleActions)
  resizeObserver.observe(root)
  resizeObserver.observe(actionSlot.value)
  window.addEventListener('scroll', scheduleActions, { passive: true })
  window.addEventListener('resize', scheduleActions)
  motion.addEventListener('change', preference)
  document.addEventListener('visibilitychange', wake)
  root.addEventListener('click', wake)
  preference()
  scheduleActions()
  cleanup = () => { revision++; flight?.cancel(); cancelAnimationFrame(request); cancelAnimationFrame(placement); observer.disconnect(); resizeObserver.disconnect(); window.removeEventListener('scroll', scheduleActions); window.removeEventListener('resize', scheduleActions); motion.removeEventListener('change', preference); document.removeEventListener('visibilitychange', wake); root.removeEventListener('click', wake) }
})
onBeforeUnmount(() => cleanup())
</script>

<template>
  <section ref="track" class="orbit-track" :class="{ 'is-static': reduced || paused }" aria-labelledby="home-title">
    <div ref="stage" class="orbit-stage">
      <div class="screen-field" aria-hidden="true"><div v-for="(screen,index) in screens" :key="index" class="orbit-screen" :style="{ '--start-x': pose(screen.phase,index).left, '--start-y': pose(screen.phase,index).top, '--start-pose': pose(screen.phase,index).transform, '--crop': screen.crop + '%', '--hue': (index % 5 - 2) * 9 + 'deg' }"><div class="glass"></div><i></i></div></div>
      <div class="watermark" aria-hidden="true"><div class="brand-relief"><img v-for="layer in 5" :key="layer" src="/brand.webp" alt="" :style="{ transform: `translateZ(${layer * 2}px)` }"></div></div>
      <div class="hero-copy"><p class="kicker"><i></i> WINDOWS REMOTE DESKTOP</p><h1 id="home-title">Evp Remote<span>.</span></h1><p class="lead">用邀请码帮亲友操作电脑，<br>或从设备列表连回自己的 Windows 桌面。</p>
        <div ref="actionSlot" class="action-slot"><Teleport to="body" :disabled="!floating"><div ref="actions" class="hero-actions" :class="{ 'actions-floating': floating, 'actions-docked': docked, 'actions-still': paused }"><ClientDownload /><a class="guide-action" href="/guide/start.html">使用指南 <span aria-hidden="true">↗</span></a></div></Teleport></div>
      </div>
      <div class="stage-foot"><span>Windows x64 客户端 0.3.1 <b>/</b> GPL-3.0-or-later</span><a href="#choose-title">向下探索 ↓</a><button v-if="!reduced" type="button" :aria-pressed="paused" @click="paused = !paused">{{ paused ? '▷ 播放动效' : 'Ⅱ 暂停动效' }}</button><span v-else>静态视图</span></div>
    </div>
  </section>
</template>
