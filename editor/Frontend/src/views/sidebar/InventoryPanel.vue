<template>
  <div class="inv-panel-shell">
    <DockTitleBar
      v-if="!isDocked"
      title="行囊"
      extraClass="bg-[#D8B86C] rounded-t-md"
      routePath="/Inventory"
      @close="closePanel"
    />

    <div class="inv-panel" @dragover.prevent="onPanelDragover" @drop.prevent="onPanelDrop">
      <span class="haze" aria-hidden="true"></span>

      <!-- ============ 头部 ============ -->
      <header class="inv-head">
        <span class="inv-seal" aria-hidden="true">
          <svg viewBox="0 0 24 24"><path d="M4 8.6c4.6.7 7.6-.4 11.4-.2" /><path d="M4.8 13c3.9.6 6.6-.3 9.6-.2" /><path d="M3.6 17.2c4.4.7 7.8-.4 11.8-.2" /></svg>
        </span>
        <h1 class="inv-title">行囊</h1>
        <span class="inv-sub">無常劫 · 隨身所負</span>
        <span class="inv-purse" title="随身金铢"><span class="inv-coin" aria-hidden="true"></span><span class="inv-coin-num">12,480</span></span>
      </header>

      <!-- ============ 主体 ============ -->
      <div class="inv-body">
        <!-- 左：角色 + 装备 -->
        <section class="inv-col inv-col--char" aria-label="披掛">
          <div class="sec-head">
            <span class="sec-dot" aria-hidden="true"></span>
            <span class="sec-txt">披掛</span>
            <span class="sec-meta">{{ gearFilled }} / {{ SLOTS.length }}</span>
          </div>

          <div class="doll">
            <!-- 左列：护甲 -->
            <div class="doll-col doll-col--arm">
              <button
                v-for="s in SLOTS.filter((x) => x.zone === 'arm')"
                :key="s.id"
                type="button"
                class="eslot"
                :class="gearCls(s.id)"
                :data-slot="s.id"
                :aria-label="slotAria(s.id)"
                draggable="true"
                @click="onEslotClick(s.id)"
                @dblclick="onEslotDbl(s.id)"
                @pointerover="onEslotOver($event, s.id)"
                @pointerout="onEslotOut"
                @dragstart="onEslotDragStart($event, s.id)"
                @dragover="onEslotDragOver($event, s.id)"
                @drop="onEslotDrop($event, s.id)"
              >
                <span class="eslot-ph">{{ slotName(s.id) }}</span>
                <span v-if="gear[s.id]" class="icon" :class="'r-' + gear[s.id].rarity"><svg viewBox="0 0 48 48"><use :href="'#' + gear[s.id].glyph" /></svg></span>
              </button>
            </div>

            <!-- 中央：角色 -->
            <div class="figure" :class="{ 'is-hurt': player.hp <= player.hpMax * 0.3, 'is-hungry': player.hunger <= player.hungerMax * 0.3 }">
              <span class="fig-badge fig-badge--atk" :class="{ off: !atkPoints }"><svg viewBox="0 0 48 48"><use href="#g-sword" /></svg><b>{{ atkPoints }}</b></span>
              <span class="fig-badge fig-badge--armor" :class="{ off: !armorPoints }"><svg viewBox="0 0 48 48"><use href="#g-shield" /></svg><b>{{ armorPoints }}</b></span>
              <div class="fig-char" v-html="charSvg"></div>
              <span v-if="gear.main" class="wep wep--main" :class="'r-' + gear.main.rarity"><svg viewBox="0 0 48 48"><use :href="'#' + gear.main.glyph" /></svg></span>
              <span v-if="gear.off" class="wep wep--off" :class="'r-' + gear.off.rarity"><svg viewBox="0 0 48 48"><use :href="'#' + gear.off.glyph" /></svg></span>
              <span v-if="gear.amulet" class="wep wep--amu" :class="'r-' + gear.amulet.rarity"><svg viewBox="0 0 48 48"><use :href="'#' + gear.amulet.glyph" /></svg></span>
              <div class="fig-hp" role="progressbar" aria-label="角色生命" :aria-valuenow="player.hp" aria-valuemin="0" :aria-valuemax="player.hpMax">
                <span class="fig-hp__fill" :style="{ width: hpPct }"></span>
              </div>
              <span class="fig-tag">無常行者</span>
            </div>

            <!-- 右列：主副手 + 饰品 -->
            <div class="doll-col doll-col--hand">
              <button
                v-for="s in SLOTS.filter((x) => x.zone === 'hand')"
                :key="s.id"
                type="button"
                class="eslot"
                :class="gearCls(s.id)"
                :data-slot="s.id"
                :aria-label="slotAria(s.id)"
                draggable="true"
                @click="onEslotClick(s.id)"
                @dblclick="onEslotDbl(s.id)"
                @pointerover="onEslotOver($event, s.id)"
                @pointerout="onEslotOut"
                @dragstart="onEslotDragStart($event, s.id)"
                @dragover="onEslotDragOver($event, s.id)"
                @drop="onEslotDrop($event, s.id)"
              >
                <span class="eslot-ph">{{ slotName(s.id) }}</span>
                <span v-if="gear[s.id]" class="icon" :class="'r-' + gear[s.id].rarity"><svg viewBox="0 0 48 48"><use :href="'#' + gear[s.id].glyph" /></svg></span>
              </button>
            </div>
          </div>
        </section>

        <!-- 右：炼化 + 状态 + 背包 -->
        <section class="inv-col inv-col--main" aria-label="行囊内容">
          <!-- 炼化 -->
          <div class="craft">
            <div class="sec-head">
              <span class="sec-dot" aria-hidden="true"></span>
              <span class="sec-txt">炼化</span>
            </div>
            <div class="craft-row">
              <div class="cgrid">
                <button
                  v-for="ci in 4"
                  :key="ci - 1"
                  type="button"
                  class="cell ccell"
                  :class="craftCls(ci - 1)"
                  :data-ci="ci - 1"
                  draggable="true"
                  @click="onCraftClick(ci - 1)"
                  @dblclick="onCraftDbl(ci - 1)"
                  @pointerover="onCraftOver($event, ci - 1)"
                  @pointerout="onCellOut"
                  @dragstart="onCraftDragStart($event, ci - 1)"
                  @dragover="onCraftDragOver($event, ci - 1)"
                  @drop="onCraftDrop($event, ci - 1)"
                >
                  <span v-if="craft[ci - 1]" class="icon" :class="'r-' + craft[ci - 1].rarity"><svg viewBox="0 0 48 48"><use :href="'#' + craft[ci - 1].glyph" /></svg></span>
                  <span v-if="craft[ci - 1] && craft[ci - 1].qty > 1" class="qty">{{ craft[ci - 1].qty }}</span>
                </button>
              </div>
              <span class="craft-arrow" aria-hidden="true">→</span>
              <button
                type="button"
                class="cell ccell ccell--result"
                :class="craftResult ? 'has r-' + craftResult.rarity : ''"
                aria-label="炼成之物"
                title="点取炼成之物"
                @click="takeResult"
                @pointerover="onResultOver"
                @pointerout="onCellOut"
              >
                <span v-if="craftResult" class="icon" :class="'r-' + craftResult.rarity"><svg viewBox="0 0 48 48"><use :href="'#' + craftResult.glyph" /></svg></span>
                <span v-else class="ccell-q">?</span>
              </button>
            </div>
          </div>

          <!-- 状态 -->
          <div class="status" aria-label="人物状态">
            <div class="stat">
              <span class="stat-ico stat-ico--hp"><svg viewBox="0 0 48 48"><use href="#g-heart" /></svg></span>
              <span class="stat-name">生命</span>
              <div class="bar bar--hp"><span class="bar-lag" :style="{ width: hpLagPct }"></span><span class="bar-fill" :style="{ width: hpPct }"></span></div>
              <span class="stat-num">{{ Math.ceil(player.hp) }}/{{ player.hpMax }}</span>
            </div>
            <div class="stat">
              <span class="stat-ico stat-ico--food"><svg viewBox="0 0 48 48"><use href="#g-meat" /></svg></span>
              <span class="stat-name">饥饿</span>
              <div class="bar bar--food"><span class="bar-lag" :style="{ width: hungerLagPct }"></span><span class="bar-fill" :style="{ width: hungerPct }"></span></div>
              <span class="stat-num">{{ Math.ceil(player.hunger) }}/{{ player.hungerMax }}</span>
            </div>
            <div class="stat">
              <span class="stat-ico stat-ico--arm"><svg viewBox="0 0 48 48"><use href="#g-shield" /></svg></span>
              <span class="stat-name">护甲</span>
              <div class="bar bar--arm"><span class="bar-fill" :style="{ width: armorPct }"></span></div>
              <span class="stat-num">{{ armorPoints }}</span>
            </div>
            <div class="stat">
              <span class="stat-ico stat-ico--xp"><svg viewBox="0 0 48 48"><use href="#g-xp" /></svg></span>
              <span class="stat-name">境界 Lv.{{ player.level }}</span>
              <div class="bar bar--xp"><span class="bar-fill" :style="{ width: xpPct }"></span></div>
              <span class="stat-num">{{ player.xp }}/{{ xpNeed }}</span>
            </div>
          </div>

          <!-- 背包格阵 -->
          <div class="grid-wrap">
            <div class="grid">
              <button
                v-for="(cell, idx) in bag"
                :key="idx"
                type="button"
                class="cell"
                :class="cellCls(idx)"
                :data-idx="idx"
                :aria-label="cellAria(idx)"
                :style="{ '--i': idx % 9 }"
                draggable="true"
                @click="onCellClick(idx)"
                @dblclick="onCellDbl(idx)"
                @pointerover="onCellOver($event, idx)"
                @pointerout="onCellOut"
                @dragstart="onCellDragStart($event, idx)"
                @dragover="onCellDragOver($event, idx)"
                @drop="onCellDrop($event, idx)"
              >
                <span v-if="cell" class="icon" :class="'r-' + cell.rarity"><svg viewBox="0 0 48 48"><use :href="'#' + cell.glyph" /></svg></span>
                <span v-if="cell && cell.qty > 1" class="qty">{{ cell.qty }}</span>
              </button>
            </div>
          </div>

          <!-- 详情 -->
          <div class="detail" v-if="selItem" :class="'r-' + selItem.rarity">
            <div class="detail-preview">
              <span class="icon" :class="'r-' + selItem.rarity"><svg viewBox="0 0 48 48"><use :href="'#' + selItem.glyph" /></svg></span>
            </div>
            <div class="detail-info">
              <h2 class="detail-name">{{ selItem.name }}<span class="detail-rarity" :class="'r-' + selItem.rarity">{{ RARITY[selItem.rarity] }}</span><span v-if="selItem.qty > 1" class="detail-qty">× {{ selItem.qty }}</span></h2>
              <p class="detail-type">{{ typeLine(selItem) }}</p>
              <div class="detail-stats">
                <div v-for="(pair, pi) in selItem.stats" :key="pi" class="detail-stat-row"><span>{{ pair[0] }}</span><b>{{ pair[1] }}</b></div>
              </div>
              <div class="detail-acts">
                <button v-if="selItem.cat === 'equip'" type="button" class="dbtn" @click="toggleEquipFromDetail">{{ selWhere === 'gear' ? '卸下' : '披掛' }}</button>
                <button v-if="selItem.cat === 'usable'" type="button" class="dbtn" @click="useSelected">服用</button>
                <button v-if="selWhere === 'craft'" type="button" class="dbtn" @click="returnToBag">收回</button>
                <button type="button" class="dbtn dbtn--ghost" @click="dropSelected">{{ selItem.cat === 'equip' ? '熔去' : '弃之' }}</button>
              </div>
            </div>
          </div>
          <p v-else class="detail-empty">未择一物 · 点选囊中器物以观其详</p>
        </section>
      </div>

      <!-- 底栏 -->
      <footer class="inv-foot">
        <span class="foot-meter"><span class="foot-name">囊中</span><b>{{ bagUsed }}</b> / {{ bag.length }}</span>
        <span class="foot-meter"><span class="foot-name">负重</span><b>{{ weight.toFixed(1) }}</b> / {{ WEIGHT_MAX }}</span>
        <span class="foot-hints">单击选取 · 双击披掛/服用 · 拖拽安放 · <b>拖出面板弃置</b></span>
      </footer>
    </div>

    <!-- 跟随光标的浮签 -->
    <div ref="tipEl" class="tip" role="tooltip">
      <p v-if="tip" class="tip-name">{{ tip.name }}<span class="tip-rarity" :class="'r-' + tip.rarity">{{ RARITY[tip.rarity] }}</span></p>
      <p v-if="tip" class="tip-type">{{ typeLine(tip) }}</p>
      <div v-if="tip" class="tip-stats">
        <div v-for="(pair, pi) in tip.stats" :key="pi"><span>{{ pair[0] }}</span><b>{{ pair[1] }}</b></div>
      </div>
      <p v-if="tip" class="tip-flavor">{{ tip.flavor }}</p>
    </div>

    <!-- 提示语 -->
    <div ref="toastEl" class="toast" role="status" aria-live="polite">{{ toastText }}</div>

    <!-- 拖出面板时的“弃”指示 -->
    <div ref="discardEl" class="discard" aria-hidden="true">弃</div>

    <!-- 图标符号库 -->
    <svg class="svgdefs" aria-hidden="true" focusable="false">
      <defs>
        <filter id="fBrush" x="-25%" y="-45%" width="150%" height="190%">
          <feTurbulence type="fractalNoise" baseFrequency="0.055 0.09" numOctaves="3" seed="11" result="n" />
          <feDisplacementMap in="SourceGraphic" in2="n" scale="4.6" xChannelSelector="R" yChannelSelector="G" />
        </filter>
        <g id="g-sword"><path d="M24 42V9" /><path d="M24 9l-5 7h10z" /><path d="M6 42h36" /><path d="M24 42l-7-8" /></g>
        <g id="g-axe"><path d="M15 7v34" /><path d="M31 9C22.5 8.5 15.6 12.7 15.5 19.5 15.4 25 19.6 28.8 25 29" /><path d="M31 9c5 1.4 9.3 5 12 9-5.6 2.2-12 1.6-17-1.6" /></g>
        <g id="g-bow"><path d="M14 8C31 15 31 33 14 40" /><path d="M14 8L14 40" /><path d="M11 24h27" /><path d="M34 19l6 5-6 5" /></g>
        <g id="g-staff"><path d="M36 5C19 15 12 31 9 43" /><path d="M25 17l11-11" /><path d="M31 10l6 5" /><circle cx="33" cy="10" r="3" /></g>
        <g id="g-helmet"><path d="M10 33c0-10 6-18 14-18s14 8 14 18" /><path d="M8 33h32" /><path d="M24 15v18" /><path d="M17 24h14" /></g>
        <g id="g-armor"><path d="M24 6l12 4v11c0 9-5.5 16.5-12 21-6.5-4.5-12-12-12-21V10z" /><path d="M18 18h12" /><path d="M24 13v14" /></g>
        <g id="g-belt"><path d="M4 21h40v6H4z" /><path d="M31 17v14" /><path d="M17 17v14" /></g>
        <g id="g-boots"><path d="M17 6v19l-8 8v3h9V6z" /><path d="M31 6v19l8 8v-3" /><path d="M31 6h-6" /><path d="M6 36h36" /></g>
        <g id="g-ring"><circle cx="24" cy="24" r="10" /><path d="M24 14v-6" /><path d="M20 5h8" /><path d="M24 10l-3 4h6z" /></g>
        <g id="g-elixir"><path d="M19 5h10v6" /><path d="M21 11c-7 4.4-9 10.4-6.5 16.6C17 33.8 22.4 36 24 36s7-2.2 9.5-8.4C36 21.4 34 15.4 27 11" /><path d="M13 27h22" /></g>
        <g id="g-pill"><path d="M24 5l14 10.5v17L24 43 10 32.5v-17z" /><path d="M10 15.5l14 10 14-10" /><path d="M24 25.5V43" /></g>
        <g id="g-scroll"><path d="M13 8h22v30H13z" /><path d="M18 16h12" /><path d="M18 22h12" /><path d="M18 28h7" /></g>
        <g id="g-talis"><path d="M17 7h14v6H17z" /><path d="M18 13c-2 12 1 22 6 30 5-8 8-18 6-30" /><path d="M21 22h6" /></g>
        <g id="g-ore"><path d="M14 15l10-8 10 8-4 15-12 0z" /><path d="M14 15h20" /><path d="M24 7v23" /><path d="M24 30v13" /></g>
        <g id="g-herb"><path d="M24 42V13" /><path d="M24 19c-6-1-10-6-10-11 6-.6 10 4 10 11" /><path d="M24 27c6-1.4 10-6.6 10-12-6-.6-10 4.8-10 12" /><path d="M14 42h20" /></g>
        <g id="g-fang"><path d="M21 5l6 8-3 26" /><path d="M27 13l7 6-6 4" /><path d="M19 41l3-4" /></g>
        <g id="g-silk"><path d="M8 17c7-6.4 14 6.4 21 0s9 .4 11 3" /><path d="M8 28c7-6.4 14 6.4 21 0s9 .4 11 3" /></g>
        <g id="g-coal"><path d="M13 28l5-15 12 4 5 13-11 9z" /><path d="M18 13l-5 15" /><path d="M30 17l5 13" /></g>
        <g id="g-meat"><path d="M11 9h26v30H11z" /><path d="M11 19h26M11 29h26M20 9v30M29 9v30" /></g>
        <g id="g-heart"><path d="M24 43C12 32 6 24 6 16.5 6 11 10 7 15 7c3.6 0 6.4 1.8 9 5.2C26.6 8.8 29.4 7 33 7c5 0 9 4 9 9.5C42 24 36 32 24 43z" /></g>
        <g id="g-shield"><path d="M24 5l16 6.5V25c0 9.8-6.4 17-16 21.5C14.4 42 8 34.8 8 25V11.5z" /><path d="M16.5 23l5.5 5.5L32 17.5" /></g>
        <g id="g-xp"><path d="M24 5l4.5 14.5L43 24l-14.5 4.5L24 43l-4.5-14.5L5 24l14.5-4.5z" /></g>
      </defs>
    </svg>
  </div>
</template>

<script setup>
import { ref, reactive, computed, inject, onMounted, onBeforeUnmount } from 'vue';
import DockTitleBar from '@/components/ui/DockTitleBar.vue';
import { useDockPanel } from '@/composables/useDockPanel.js';

const { isDocked, closePanel } = useDockPanel();
const inDock = inject('inDock', false);

/* ================= 静态数据 ================= */
const RARITY = { common: '凡品', fine: '良品', rare: '珍品', epic: '秘宝' };
const RARITY_WEIGHT = { common: 1, fine: 2, rare: 3, epic: 4 };

const SLOTS = [
  { id: 'helm', name: '头盔', zone: 'arm', types: ['重甲', '轻甲'] },
  { id: 'armor', name: '战衣', zone: 'arm', types: ['重甲', '轻甲'] },
  { id: 'belt', name: '腰系', zone: 'arm', types: ['腰系'] },
  { id: 'boots', name: '足履', zone: 'arm', types: ['靴履'] },
  { id: 'main', name: '主兵', zone: 'hand', types: ['长兵', '刀剑', '弓弩', '法器'] },
  { id: 'off', name: '副兵', zone: 'hand', types: ['刀剑', '法器', '弓弩', '长兵'] },
  { id: 'amulet', name: '护符', zone: 'hand', types: ['护符'] },
  { id: 'ring', name: '指环', zone: 'hand', types: ['佩环'] },
];
const SLOT_BY_ID = Object.fromEntries(SLOTS.map((s) => [s.id, s]));

const ITEMS = [
  { u: 'armor-1', name: '影纹鳞甲', type: '重甲', cat: 'equip', slot: 'armor', rarity: 'epic', glyph: 'g-armor', armor: 8, stats: [['护体', '+186'], ['筋骨', '+24'], ['抗蚀', '+18%']], flavor: '鳞片取自深潭老蛟，贴着火光看，纹路会自己游动。' },
  { u: 'main-1', name: '赤霄长兵', type: '长兵', cat: 'equip', slot: 'main', rarity: 'epic', glyph: 'g-sword', atk: 12, stats: [['锋芒', '86 - 124'], ['力道', '+31'], ['破甲', '+12%']], flavor: '刃上缠着一线不散的血气，主人不问，它也不说。' },
  { u: 'helm-1', name: '兜鍪 · 静水', type: '重甲', cat: 'equip', slot: 'helm', rarity: 'rare', glyph: 'g-helmet', armor: 4, stats: [['护体', '+92'], ['定神', '+14']], flavor: '面甲内侧刻着半句残咒，据说是铸者留给自己的。' },
  { u: 'amulet-1', name: '青囊护符', type: '护符', cat: 'equip', slot: 'amulet', rarity: 'rare', glyph: 'g-talis', armor: 1, stats: [['定神', '+22'], ['回气', '+8/s']], flavor: '符纸换了七次，绳结始终没舍得拆。' },
  { u: 'boots-1', name: '踏雾履', type: '靴履', cat: 'equip', slot: 'boots', rarity: 'rare', glyph: 'g-boots', armor: 2, stats: [['身法', '+19'], ['疾行', '+9%']], flavor: '踩在松针上，声音比风还迟一步。' },
  { u: 'belt-1', name: '缠云腰带', type: '腰系', cat: 'equip', slot: 'belt', rarity: 'fine', glyph: 'g-belt', armor: 3, stats: [['护体', '+38'], ['负重', '+12']], flavor: '三层素绢，一层一线都是山里人自己纺的。' },
  { u: 'ring-1', name: '残玉指环', type: '佩环', cat: 'equip', slot: 'ring', rarity: 'fine', glyph: 'g-ring', armor: 1, stats: [['锋芒', '+9'], ['回气', '+3/s']], flavor: '玉上有一道旧裂，握紧时微微发烫。' },
  { u: 'off-1', name: '断水短刃', type: '刀剑', cat: 'equip', slot: 'off', rarity: 'fine', glyph: 'g-sword', atk: 5, stats: [['锋芒', '42 - 58'], ['身法', '+11']], flavor: '短得只能贴身用，也近得让人来不及退。' },
  { u: 'main-2', name: '乌木猎弓', type: '弓弩', cat: 'equip', slot: 'main', rarity: 'fine', glyph: 'g-bow', atk: 8, stats: [['锋芒', '56 - 74'], ['力道', '+14']], flavor: '弦是旧弦，换过三次弓臂，准头反而更稳。' },
  { u: 'main-3', name: '镇魂法铃', type: '法器', cat: 'equip', slot: 'main', rarity: 'rare', glyph: 'g-staff', atk: 9, stats: [['术法', '+27'], ['定神', '+16']], flavor: '摇一下，活人听见的是铃，别的东西听见的是雷。' },
  { u: 'off-2', name: '开山短斧', type: '刀剑', cat: 'equip', slot: 'off', rarity: 'common', glyph: 'g-axe', atk: 4, stats: [['锋芒', '33 - 45'], ['力道', '+8']], flavor: '斧背豁了几处口，砍柴砍人都不耽误。' },
  { u: 'use-1', name: '回春丹', type: '丹散', cat: 'usable', rarity: 'fine', glyph: 'g-pill', qty: 12, heal: 6, xp: 5, stats: [['回复生命', '6'], ['参悟', '+5']], flavor: '入口先苦后甘，苦的那口才是药。' },
  { u: 'use-2', name: '凝神散', type: '丹散', cat: 'usable', rarity: 'fine', glyph: 'g-pill', qty: 8, heal: 2, xp: 12, stats: [['回复生命', '2'], ['参悟', '+12']], flavor: '化在舌下，像咽了一口山里的凉雾。' },
  { u: 'use-3', name: '青铜小还丹', type: '丹散', cat: 'usable', rarity: 'rare', glyph: 'g-elixir', qty: 3, heal: 10, xp: 18, stats: [['回复生命', '10'], ['参悟', '+18']], flavor: '丹衣上浮着铜绿，老药师说这是它睡醒的样子。' },
  { u: 'use-4', name: '朱砂符纸', type: '符纸', cat: 'usable', rarity: 'fine', glyph: 'g-scroll', qty: 5, xp: 30, stats: [['参悟', '+30']], flavor: '画符的人手很稳，最后那一笔却总爱往上挑。' },
  { u: 'food-1', name: '风干兽肉', type: '食物', cat: 'usable', rarity: 'common', glyph: 'g-meat', qty: 6, food: 6, heal: 1, stats: [['恢复饥饿', '6'], ['恢复生命', '1']], flavor: '盐巴和山风腌出来的，硬得能敲核桃。' },
  { u: 'food-2', name: '野菜团子', type: '食物', cat: 'usable', rarity: 'common', glyph: 'g-herb', qty: 9, food: 4, stats: [['恢复饥饿', '4']], flavor: '苦菜混着粗粮，嚼起来沙沙的。' },
  { u: 'mat-1', name: '玄铁矿', type: 'material', cat: 'mat', rarity: 'common', glyph: 'g-ore', qty: 24, stats: [['锻造', '可用']], flavor: '敲开来，断口里有一线细细的黑光。' },
  { u: 'mat-2', name: '铜绿矿脉', type: 'material', cat: 'mat', rarity: 'fine', glyph: 'g-ore', qty: 9, stats: [['锻造', '上品']], flavor: '埋得越深，颜色越像雨后旧钟。' },
  { u: 'mat-3', name: '幽昙草', type: 'material', cat: 'mat', rarity: 'fine', glyph: 'g-herb', qty: 14, stats: [['炼丹', '可用']], flavor: '子时开，丑时谢，采药的人从不点灯。' },
  { u: 'mat-4', name: '蚀骨妖牙', type: 'material', cat: 'mat', rarity: 'rare', glyph: 'g-fang', qty: 2, stats: [['锻造', '秘材']], flavor: '牙根还带着温，剥下来时整片林子都静了。' },
  { u: 'mat-5', name: '地脉残炭', type: 'material', cat: 'mat', rarity: 'common', glyph: 'g-coal', qty: 31, stats: [['燃料', '耐烧']], flavor: '燃起来无烟，火色是很少见的青。' },
  { u: 'mat-6', name: '蚕丝云缎', type: 'material', cat: 'mat', rarity: 'fine', glyph: 'g-silk', qty: 6, stats: [['缝制', '上品']], flavor: '抖开像一小片云，落在手上几乎没有分量。' },
];
const BY_U = Object.fromEntries(ITEMS.map((d) => [d.u, d]));

const LOADOUT = { main: 'main-1', off: 'off-1', armor: 'armor-1', helm: 'helm-1', amulet: 'amulet-1', belt: 'belt-1', boots: 'boots-1', ring: 'ring-1' };

/* 2×2 炼化配方：in 为 4 格物品 uid（空位 null），out 为结果物品 uid */
const RECIPES = [
  { in: ['mat-1', 'mat-1', null, null], out: 'mat-2' },
  { in: ['mat-3', 'mat-3', null, null], out: 'use-1' },
  { in: ['mat-5', 'mat-6', null, null], out: 'use-4' },
];

const WEIGHT_MAX = 120;
const BAG_SIZE = 36; // 27 主包 + 9 快捷

/* ================= 运行时状态 ================= */
let uidSeq = 0;
function makeItem(def) {
  const it = { ...def };
  it.uid = `${def.u}#${++uidSeq}`;
  it.qty = def.qty || 1;
  return it;
}

function slotsFor(item) {
  if (!item || item.cat !== 'equip') return [];
  return SLOTS.filter((s) => s.types.includes(item.type)).map((s) => s.id);
}

const player = reactive({ hp: 20, hpMax: 20, hunger: 20, hungerMax: 20, xp: 0, level: 1 });
const gear = reactive({});
const bag = ref([]);
const craft = reactive([null, null, null, null]);
const craftResult = ref(null);
const sel = ref(null); // uid
const drag = ref(null); // { where, idx/slot, uid }
const dragConsumed = ref(false);

/* 拖拽/提示 DOM 引用 */
const tipEl = ref(null);
const toastEl = ref(null);
const discardEl = ref(null);
const tip = ref(null);
const toastText = ref('');
const tipVisible = ref(false);
let toastTimer = null;
let tipTimer = null;

const clamp = (v, a, b) => Math.min(b, Math.max(a, v));

function initData() {
  const equipDefs = ITEMS.filter((d) => d.cat === 'equip');
  const restDefs = ITEMS.filter((d) => d.cat !== 'equip');
  Object.keys(LOADOUT).forEach((sid) => {
    const d = BY_U[LOADOUT[sid]];
    if (d) gear[sid] = makeItem(d);
  });
  const pool = [];
  equipDefs.forEach((d) => { if (!Object.values(LOADOUT).includes(d.u)) pool.push(makeItem(d)); });
  restDefs.forEach((d) => pool.push(makeItem(d)));
  for (let i = pool.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [pool[i], pool[j]] = [pool[j], pool[i]];
  }
  const total = BAG_SIZE;
  const floorCount = Math.min(pool.length, Math.round(total * 0.72));
  const cells = [];
  for (let i = 0; i < total; i++) {
    let it = null;
    const mustFill = total - i <= pool.length;
    const wantFill = pool.length && (i < floorCount || Math.random() < 0.55);
    if (pool.length && (mustFill || wantFill)) it = pool.pop();
    cells.push(it);
  }
  bag.value = cells;
}

/* ================= 派生 ================= */
const armorPoints = computed(() => Object.values(gear).reduce((sum, it) => sum + (it ? it.armor || 0 : 0), 0));
const atkPoints = computed(() => Object.values(gear).reduce((sum, it) => sum + (it ? it.atk || 0 : 0), 0));
const gearFilled = computed(() => Object.values(gear).filter(Boolean).length);
const bagUsed = computed(() => bag.value.filter(Boolean).length);
const weight = computed(() => {
  let w = 0;
  Object.values(gear).forEach((it) => { if (it) w += itemWeight(it); });
  bag.value.forEach((it) => { if (it) w += itemWeight(it); });
  return w;
});
const xpNeed = computed(() => player.level * 50);
const hpPct = computed(() => `${clamp((player.hp / player.hpMax) * 100, 0, 100).toFixed(1)}%`);
const hungerPct = computed(() => `${clamp((player.hunger / player.hungerMax) * 100, 0, 100).toFixed(1)}%`);
const armorPct = computed(() => `${clamp((armorPoints.value / 20) * 100, 0, 100).toFixed(1)}%`);
const xpPct = computed(() => `${clamp((player.xp / xpNeed.value) * 100, 0, 100).toFixed(1)}%`);
const hpLagPct = ref('100%');
const hungerLagPct = ref('100%');

const selItem = computed(() => {
  const found = findItemByUid(sel.value);
  return found ? found.item : null;
});
const selWhere = computed(() => {
  const found = findItemByUid(sel.value);
  return found ? found.where : null;
});

function itemWeight(it) {
  return (RARITY_WEIGHT[it.rarity] * 0.5 + (it.cat === 'equip' ? 2.2 : 0.3)) * it.qty;
}

function findItemByUid(uid) {
  for (const k in gear) if (gear[k] && gear[k].uid === uid) return { item: gear[k], where: 'gear', slot: k };
  for (let i = 0; i < bag.value.length; i++) if (bag.value[i] && bag.value[i].uid === uid) return { item: bag.value[i], where: 'bag', idx: i };
  for (let i = 0; i < 4; i++) if (craft[i] && craft[i].uid === uid) return { item: craft[i], where: 'craft', idx: i };
  return null;
}

function typeLine(it) {
  let s = it.type;
  if (it.cat === 'equip') {
    const names = slotsFor(it).map((id) => SLOT_BY_ID[id].name).join(' / ');
    s += ` · 可安放：${names || '—'}`;
  } else if (it.cat === 'usable') {
    s += ' · 随身可用';
  } else {
    s += ' · 锻造炼药之材';
  }
  return s;
}

/* ================= 角色 SVG ================= */
const charSvg = computed(() => {
  const skin = '#d0a06b', hair = '#241d16', shirt = '#4a3e31', shirtD = '#3a3025', pants = '#2c241b', pantsD = '#221b14', ink = '#171310', gold = '#c8a659', goldD = '#8a7038', goldL = '#f0d68f';
  let s = '';
  s += '<rect x="8" y="0" width="16" height="16" fill="' + skin + '"/>';
  s += '<rect x="8" y="0" width="16" height="5" fill="' + hair + '"/>';
  s += '<rect x="13" y="-2" width="6" height="4" rx="2" fill="' + hair + '"/>';
  s += '<rect x="11" y="8" width="2.2" height="2.6" fill="' + ink + '"/>';
  s += '<rect x="19" y="8" width="2.2" height="2.6" fill="' + ink + '"/>';
  s += '<rect x="9" y="12.5" width="14" height="1.6" fill="' + ink + '" opacity=".55"/>';
  s += '<rect x="8" y="16" width="16" height="24" fill="' + shirt + '"/>';
  s += '<path d="M12 16h8v4h-8z" fill="' + shirtD + '"/>';
  s += '<rect x="13.6" y="16" width="4.8" height="24" fill="' + ink + '" opacity=".14"/>';
  s += '<rect x="0" y="16" width="8" height="20" fill="' + shirt + '"/>';
  s += '<rect x="24" y="16" width="8" height="20" fill="' + shirt + '"/>';
  s += '<rect x="0" y="36" width="8" height="4" fill="' + skin + '"/>';
  s += '<rect x="24" y="36" width="8" height="4" fill="' + skin + '"/>';
  s += '<rect x="8" y="40" width="8" height="20" fill="' + pants + '"/>';
  s += '<rect x="16" y="40" width="8" height="20" fill="' + pants + '"/>';
  s += '<rect x="8" y="40" width="8" height="4" fill="' + pantsD + '"/>';
  s += '<rect x="16" y="40" width="8" height="4" fill="' + pantsD + '"/>';
  s += '<rect x="6" y="58" width="10" height="6" rx="1" fill="' + pantsD + '"/>';
  s += '<rect x="16" y="58" width="10" height="6" rx="1" fill="' + pantsD + '"/>';
  if (gear.helm) s += '<g class="ov ov-helm"><rect x="6" y="-2" width="20" height="18" rx="2" fill="' + gold + '" stroke="' + goldD + '" stroke-width=".8"/><rect x="6" y="11" width="20" height="3" fill="' + goldL + '" opacity=".55"/><rect x="14" y="-4" width="4" height="4" fill="#e0523b" transform="rotate(45 16 -2)"/></g>';
  if (gear.armor) s += '<g class="ov ov-chest"><rect x="5" y="14" width="22" height="27" rx="2" fill="' + gold + '" stroke="' + goldD + '" stroke-width=".8"/><rect x="-1" y="15" width="9" height="8" rx="1.5" fill="' + goldD + '"/><rect x="24" y="15" width="9" height="8" rx="1.5" fill="' + goldD + '"/><rect x="5" y="24" width="22" height="2.4" fill="' + goldL + '" opacity=".4"/><path d="M13 15v26" stroke="' + goldL + '" stroke-width=".9" opacity=".5"/></g>';
  if (gear.belt) s += '<g class="ov ov-legs"><rect x="7" y="38" width="18" height="17" rx="1.5" fill="' + goldD + '" stroke="#5c4a20" stroke-width=".6"/><rect x="9.5" y="40" width="6" height="15" fill="' + gold + '" opacity=".85"/><rect x="16.5" y="40" width="6" height="15" fill="' + gold + '" opacity=".85"/><rect x="13" y="36.5" width="6" height="5" fill="' + goldL + '" transform="rotate(45 16 39)"/></g>';
  if (gear.boots) s += '<g class="ov ov-boots"><rect x="4" y="56" width="12" height="9" rx="1.2" fill="' + goldD + '"/><rect x="16" y="56" width="12" height="9" rx="1.2" fill="' + goldD + '"/><rect x="4" y="56" width="12" height="2.4" fill="' + goldL + '" opacity=".5"/><rect x="16" y="56" width="12" height="2.4" fill="' + goldL + '" opacity=".5"/></g>';
  return '<svg viewBox="0 0 32 64" preserveAspectRatio="xMidYMid meet" class="char-svg">' + s + '</svg>';
});

/* ================= 状态/经验 ================= */
function grantXP(n) {
  if (!n) return;
  player.xp += n;
  while (player.xp >= xpNeed.value) {
    player.xp -= xpNeed.value;
    player.level += 1;
    toast('升阶 · 境 ' + player.level);
  }
}

function syncPlayerBars() {
  const oldHp = parseFloat(hpLagPct.value) || 100;
  hpLagPct.value = hpPct.value;
  setTimeout(() => { if (hpLagPct.value === hpPct.value) { /* 追赶完成 */ } }, 650);
  void oldHp;
  const oldHunger = parseFloat(hungerLagPct.value) || 100;
  hungerLagPct.value = hungerPct.value;
  void oldHunger;
}

function applyHeal(n) { player.hp = clamp(player.hp + (n || 0), 0, player.hpMax); }
function applyFood(n) { player.hunger = clamp(player.hunger + (n || 0), 0, player.hungerMax); }

/* ================= 装备/使用/丢弃 ================= */
function equipFromBag(idx, preferredSlot) {
  const it = bag.value[idx];
  if (!it || it.cat !== 'equip') { toast('此物无法披掛'); return; }
  let sid = preferredSlot;
  if (!sid || !slotsFor(it).includes(sid)) sid = slotsFor(it)[0];
  if (!sid) { toast('无处安放'); return; }
  const old = gear[sid] || null;
  gear[sid] = it;
  bag.value[idx] = old;
  sel.value = it.uid;
  grantXP(RARITY_WEIGHT[it.rarity]);
  toast('披掛 · ' + it.name);
}

function unequip(sid) {
  const it = gear[sid];
  if (!it) return;
  const empty = bag.value.findIndex((c) => !c);
  if (empty < 0) { toast('囊中已满'); return; }
  bag.value[empty] = it;
  gear[sid] = null;
  sel.value = it.uid;
  toast('卸下 · ' + it.name);
}

function useItemAt(idx) {
  const it = bag.value[idx];
  if (!it || it.cat !== 'usable') return;
  applyHeal(it.heal);
  applyFood(it.food);
  grantXP(it.xp);
  toast('服用 · ' + it.name);
  if (it.qty > 1) it.qty -= 1;
  else { bag.value[idx] = null; if (sel.value === it.uid) sel.value = null; }
}

function dropItem(uid) {
  const found = findItemByUid(uid);
  if (!found) return;
  const it = found.item;
  if (found.where === 'gear') gear[found.slot] = null;
  else if (found.where === 'bag') bag.value[found.idx] = null;
  else craft[found.idx] = null;
  if (sel.value === uid) sel.value = null;
  toast((it.cat === 'equip' ? '熔去' : '弃之') + ' · ' + it.name);
  computeCraft();
}

/* ================= 炼化 ================= */
function computeCraft() {
  const ids = craft.map((c) => (c ? c.u : null));
  let out = null;
  for (const r of RECIPES) {
    const a = ids.filter(Boolean).slice().sort();
    const b = r.in.filter(Boolean).slice().sort();
    if (a.length === b.length && a.every((v, i) => v === b[i])) { out = BY_U[r.out]; break; }
  }
  craftResult.value = out;
}

function takeResult() {
  if (!craftResult.value) return;
  const empty = bag.value.findIndex((c) => !c);
  if (empty < 0) { toast('囊中已满'); return; }
  const def = craftResult.value;
  bag.value[empty] = makeItem(def);
  craft.splice(0, 4, null, null, null, null);
  craftResult.value = null;
  toast('炼成 · ' + def.name);
}

function returnToBag() {
  const found = findItemByUid(sel.value);
  if (!found || found.where !== 'craft') return;
  const empty = bag.value.findIndex((c) => !c);
  if (empty < 0) { toast('囊中已满'); return; }
  bag.value[empty] = found.item;
  craft[found.idx] = null;
  sel.value = null;
  computeCraft();
  toast('收回 · ' + found.item.name);
}

/* ================= 点击/双击 ================= */
function onCellClick(idx) {
  const it = bag.value[idx];
  if (!it) return;
  sel.value = it.uid;
}

function onCellDbl(idx) {
  const it = bag.value[idx];
  if (!it) return;
  if (it.cat === 'equip') equipFromBag(idx);
  else if (it.cat === 'usable') useItemAt(idx);
  else toast('此物只堪锻造');
}

function onEslotClick(sid) {
  const it = gear[sid];
  if (!it) { sel.value = null; return; }
  sel.value = it.uid;
}

function onEslotDbl(sid) {
  if (gear[sid]) unequip(sid);
}

function onCraftClick(ci) {
  if (craft[ci]) sel.value = craft[ci].uid;
}

function onCraftDbl(ci) {
  if (!craft[ci]) return;
  const empty = bag.value.findIndex((c) => !c);
  if (empty < 0) { toast('囊中已满'); return; }
  bag.value[empty] = craft[ci];
  craft[ci] = null;
  computeCraft();
  toast('收回 · ' + bag.value[empty].name);
}

function toggleEquipFromDetail() {
  const found = findItemByUid(sel.value);
  if (!found) return;
  if (found.where === 'gear') unequip(found.slot);
  else if (found.where === 'bag') equipFromBag(found.idx);
}

function useSelected() {
  const found = findItemByUid(sel.value);
  if (found && found.where === 'bag') useItemAt(found.idx);
}

function dropSelected() {
  if (sel.value) dropItem(sel.value);
}

/* ================= 拖拽 ================= */
function takeFrom(d) {
  if (d.where === 'bag') {
    return { it: bag.value[d.idx], put: (x) => { bag.value[d.idx] = x; } };
  }
  if (d.where === 'gear') {
    return { it: gear[d.slot], put: (x) => { gear[d.slot] = x; } };
  }
  if (d.where === 'craft') {
    return { it: craft[d.idx], put: (x) => { craft[d.idx] = x; } };
  }
  return { it: null, put: () => {} };
}

function startDrag(e, d) {
  if (!d.it) { e.preventDefault(); return false; }
  drag.value = { where: d.where, idx: d.idx, slot: d.slot, uid: d.it.uid };
  dragConsumed.value = false;
  e.dataTransfer.effectAllowed = 'move';
  try { e.dataTransfer.setData('text/plain', d.it.uid); } catch (err) { /* noop */ }
  if (e.dataTransfer && e.dataTransfer.setDragImage) {
    try { e.dataTransfer.setDragImage(e.currentTarget, 16, 16); } catch (err) { /* noop */ }
  }
  return true;
}

function onCellDragStart(e, idx) {
  startDrag(e, { where: 'bag', idx, it: bag.value[idx] });
}

function onEslotDragStart(e, sid) {
  startDrag(e, { where: 'gear', slot: sid, it: gear[sid] });
}

function onCraftDragStart(e, ci) {
  startDrag(e, { where: 'craft', idx: ci, it: craft[ci] });
}

function putToBag(d, to) {
  const src = takeFrom(d);
  const it = src.it;
  if (!it) return;
  const tgt = bag.value[to];
  if (tgt && tgt.uid === it.uid) return;
  bag.value[to] = it;
  src.put(tgt);
  sel.value = it.uid;
  toast('挪动行囊');
}

function putToGear(d, sid) {
  const src = takeFrom(d);
  const it = src.it;
  if (!it) return;
  if (it.cat !== 'equip' || !slotsFor(it).includes(sid)) {
    toast('此位不容 ' + it.name);
    return;
  }
  const old = gear[sid];
  if (old && old.uid === it.uid) return;
  gear[sid] = it;
  src.put(old);
  sel.value = it.uid;
  if (d.where !== 'gear') grantXP(RARITY_WEIGHT[it.rarity]);
  toast('披掛 · ' + it.name);
}

function putToCraft(d, ci) {
  const src = takeFrom(d);
  const it = src.it;
  if (!it) return;
  const tgt = craft[ci];
  if (tgt && tgt.uid === it.uid) return;
  craft[ci] = it;
  src.put(tgt);
  sel.value = it.uid;
  computeCraft();
  toast('置入炼化');
}

function finishDrag() {
  drag.value = null;
  dragConsumed.value = false;
  hideDiscard();
}

function onCellDragOver(e, idx) {
  if (!drag.value) return;
  e.preventDefault();
  e.dataTransfer.dropEffect = 'move';
  document.body.classList.add('inv-drag-over');
}

function onCellDrop(e, idx) {
  if (!drag.value) return;
  e.preventDefault();
  dragConsumed.value = true;
  putToBag(drag.value, idx);
  finishDrag();
}

function onEslotDragOver(e, sid) {
  if (!drag.value) return;
  e.preventDefault();
  e.dataTransfer.dropEffect = 'move';
  document.body.classList.add('inv-drag-over');
}

function onEslotDrop(e, sid) {
  if (!drag.value) return;
  e.preventDefault();
  dragConsumed.value = true;
  putToGear(drag.value, sid);
  finishDrag();
}

function onCraftDragOver(e, ci) {
  if (!drag.value) return;
  e.preventDefault();
  e.dataTransfer.dropEffect = 'move';
  document.body.classList.add('inv-drag-over');
}

function onCraftDrop(e, ci) {
  if (!drag.value) return;
  e.preventDefault();
  dragConsumed.value = true;
  putToCraft(drag.value, ci);
  finishDrag();
}

/* 面板整体：拖入面板内空白区域 = 不丢弃（消费掉） */
function onPanelDragover(e) {
  if (!drag.value) return;
  e.preventDefault();
  e.dataTransfer.dropEffect = 'move';
  hideDiscard();
}

function onPanelDrop() {
  if (!drag.value) return;
  dragConsumed.value = true;
  finishDrag();
}

/* 拖出面板 = 丢弃 */
function onWindowDragover(e) {
  if (!drag.value) return;
  const panel = e.target && e.target.closest ? e.target.closest('.inv-panel') : null;
  if (!panel) {
    showDiscard(e.clientX, e.clientY);
  } else {
    hideDiscard();
  }
}

function onWindowDrop(e) {
  if (!drag.value || dragConsumed.value) return;
  const panel = e.target && e.target.closest ? e.target.closest('.inv-panel') : null;
  if (!panel) {
    e.preventDefault();
    dragConsumed.value = true;
    dropItem(drag.value.uid);
    finishDrag();
  }
}

function onDragEnd() {
  if (drag.value && !dragConsumed.value) {
    dropItem(drag.value.uid);
  }
  finishDrag();
}

/* 丢弃指示 */
function showDiscard(x, y) {
  if (!discardEl.value) return;
  const el = discardEl.value;
  el.classList.add('is-on');
  el.style.left = x + 'px';
  el.style.top = y + 'px';
}

function hideDiscard() {
  if (!discardEl.value) return;
  discardEl.value.classList.remove('is-on');
}

/* ================= 浮签 ================= */
function onCellOver(e, idx) {
  const it = bag.value[idx];
  if (it) showTip(it, e.clientX, e.clientY);
}

function onEslotOver(e, sid) {
  const it = gear[sid];
  if (it) showTip(it, e.clientX, e.clientY);
}

function onCraftOver(e, ci) {
  const it = craft[ci];
  if (it) showTip(it, e.clientX, e.clientY);
}

function onResultOver(e) {
  if (craftResult.value) showTip(craftResult.value, e.clientX, e.clientY);
}

function onCellOut() {
  hideTipSoon();
}

function showTip(item, x, y) {
  clearTimeout(tipTimer);
  tip.value = item;
  tipVisible.value = true;
  moveTip(x, y);
}

function moveTip(x, y) {
  if (!tipVisible.value || !tipEl.value) return;
  const el = tipEl.value;
  const w = el.offsetWidth || 220;
  const h = el.offsetHeight || 140;
  let left = x + 16;
  let top = y + 14;
  if (left + w > window.innerWidth - 8) left = x - w - 16;
  if (top + h > window.innerHeight - 8) top = Math.max(8, y - h - 14);
  el.style.left = Math.max(8, left) + 'px';
  el.style.top = Math.max(8, top) + 'px';
}

function hideTipSoon() {
  tipTimer = setTimeout(() => {
    tip.value = null;
    tipVisible.value = false;
  }, 80);
}

/* ================= 提示语 ================= */
function toast(text) {
  toastText.value = text;
  if (toastEl.value) {
    toastEl.value.classList.add('is-on');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toastEl.value.classList.remove('is-on'), 1400);
  }
}

/* ================= 键盘 ================= */
function onKeydown(e) {
  const k = e.key;
  if (k === 'Escape') {
    if (tipVisible.value) { hideTipSoon(); return; }
    sel.value = null;
    return;
  }
  if ((k === 'Delete' || k === 'Backspace') && sel.value) {
    e.preventDefault();
    dropItem(sel.value);
  }
  if (k === 'Enter' && sel.value) {
    const found = findItemByUid(sel.value);
    if (found && found.where === 'bag') {
      e.preventDefault();
      if (found.item.cat === 'equip') equipFromBag(found.idx);
      else if (found.item.cat === 'usable') useItemAt(found.idx);
    }
  }
}

/* 指针移动更新浮签位置 */
function onPointerMove(e) {
  if (tipVisible.value) moveTip(e.clientX, e.clientY);
}

/* ================= 工具函数（模板用） ================= */
function gearCls(sid) {
  const it = gear[sid];
  return { has: !!it, ...(it ? { ['r-' + it.rarity]: true } : {}) };
}
function cellCls(idx) {
  const it = bag.value[idx];
  return { has: !!it, 'is-sel': !!(it && it.uid === sel.value), 'is-empty': !it, ...(it ? { ['r-' + it.rarity]: true } : {}) };
}
function craftCls(ci) {
  const it = craft[ci];
  return { has: !!it, 'is-sel': !!(it && it.uid === sel.value), 'is-empty': !it, ...(it ? { ['r-' + it.rarity]: true } : {}) };
}
function slotName(sid) { return SLOT_BY_ID[sid].name; }
function slotAria(sid) {
  const it = gear[sid];
  return it ? `${SLOT_BY_ID[sid].name}：${it.name}` : `${SLOT_BY_ID[sid].name}（空）`;
}
function cellAria(idx) {
  const it = bag.value[idx];
  return it ? `${it.name} · ${it.type} · ${RARITY[it.rarity]}` : `行囊第 ${idx + 1} 格`;
}

/* ================= 生命周期 ================= */
onMounted(() => {
  initData();
  window.addEventListener('dragover', onWindowDragover);
  window.addEventListener('drop', onWindowDrop);
  document.addEventListener('dragend', onDragEnd);
  window.addEventListener('pointermove', onPointerMove);
  window.addEventListener('keydown', onKeydown);
  toast('行囊已启 · 择一物以观其详');
});

onBeforeUnmount(() => {
  window.removeEventListener('dragover', onWindowDragover);
  window.removeEventListener('drop', onWindowDrop);
  document.removeEventListener('dragend', onDragEnd);
  window.removeEventListener('pointermove', onPointerMove);
  window.removeEventListener('keydown', onKeydown);
  clearTimeout(toastTimer);
  clearTimeout(tipTimer);
});
</script>

<style scoped>
/* ================= 设计令牌（东方暗黑金墨） ================= */
.inv-panel-shell {
  width: 100%;
  height: 100%;
  min-height: 0;
  display: flex;
  flex-direction: column;
  background: #100e0c;
  color: #e9e0cc;
  font-family: 'Noto Serif SC', 'Source Han Serif SC', 'Songti SC', STSong, SimSun, serif;
  user-select: none;
  -webkit-user-select: none;
  overflow: hidden;
}
.inv-panel {
  --gold: #c8a659;
  --gold-dim: #8a7038;
  --gold-bright: #f0d68f;
  --cinnabar: #b3382a;
  --cinnabar-bright: #e0523b;
  --bronze: #5f8a72;
  --paper: #e9e0cc;
  --paper-dim: #bdb298;
  --ink: #0c0b0a;
  --s: clamp(26px, 6.6vw, 34px);
  --sg: 5px;
  --cut: 10px;
  --shape: polygon(var(--cut) 0, 100% 0, 100% calc(100% - var(--cut)), calc(100% - var(--cut)) 100%, 0 100%, 0 var(--cut));
  position: relative;
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 10px 10px 8px;
  border: 2px solid transparent;
  background:
    linear-gradient(180deg, rgba(26, 23, 18, 0.96), rgba(13, 12, 10, 0.97)) padding-box,
    repeating-linear-gradient(58deg, rgba(255, 242, 210, 0.18) 0 1px, transparent 1px 4px) border-box,
    linear-gradient(140deg, rgba(240, 214, 143, 0.85), rgba(122, 98, 52, 0.45) 52%, rgba(240, 214, 143, 0.75)) border-box;
  clip-path: var(--shape);
  overflow: hidden;
}
.haze {
  position: absolute;
  left: -16%;
  top: -45%;
  width: 64%;
  height: 190%;
  pointer-events: none;
  z-index: 0;
  background: radial-gradient(closest-side, rgba(233, 224, 204, 0.1), rgba(233, 224, 204, 0) 72%);
  filter: blur(10px);
}
.inv-panel > * { position: relative; z-index: 1; }

/* ================= 头部 ================= */
.inv-head {
  display: flex;
  align-items: center;
  gap: 8px;
  padding-bottom: 6px;
  border-bottom: 1px solid rgba(200, 166, 89, 0.22);
}
.inv-seal {
  flex: none;
  width: 22px;
  height: 22px;
  display: grid;
  place-items: center;
  border: 2px solid rgba(214, 96, 72, 0.78);
  background: linear-gradient(180deg, rgba(179, 56, 42, 0.28), rgba(179, 56, 42, 0.06));
  border-radius: 2px 6px 2px 2px;
  transform: rotate(-3deg);
}
.inv-seal svg { width: 13px; height: 13px; }
.inv-seal path { fill: none; stroke: #e0523b; stroke-width: 1.8; stroke-linecap: round; }
.inv-title {
  margin: 0;
  font-family: 'LXGW WenKai', '霞鹜文楷', 'Kaiti SC', KaiTi, serif;
  font-weight: 400;
  font-size: 17px;
  letter-spacing: 0.34em;
  text-indent: 0.34em;
  color: #f0e3c2;
  text-shadow: 0 1px 0 #000, 0 0 18px rgba(0, 0, 0, 0.9);
  white-space: nowrap;
}
.inv-sub {
  font-size: 9.5px;
  letter-spacing: 0.2em;
  color: rgba(233, 224, 204, 0.4);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  min-width: 0;
}
.inv-purse {
  margin-left: auto;
  flex: none;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 3px 8px 3px 6px;
  clip-path: var(--shape);
  border: 2px solid transparent;
  background: linear-gradient(180deg, rgba(40, 34, 26, 0.82), rgba(18, 16, 13, 0.86)) padding-box,
    linear-gradient(140deg, rgba(240, 214, 143, 0.75), rgba(122, 98, 52, 0.4) 52%, rgba(240, 214, 143, 0.65)) border-box;
}
.inv-coin {
  width: 9px;
  height: 9px;
  transform: rotate(45deg);
  background: linear-gradient(180deg, #f0d68f, #8a7038);
  box-shadow: 0 0 8px rgba(240, 214, 143, 0.55);
}
.inv-coin-num {
  font-size: 11px;
  font-variant-numeric: tabular-nums;
  color: #f0d68f;
  letter-spacing: 0.06em;
}

/* ================= 主体 ================= */
.inv-body {
  flex: 1;
  min-height: 0;
  display: flex;
  gap: 8px;
}
.inv-col {
  display: flex;
  flex-direction: column;
  gap: 6px;
  min-height: 0;
}
.inv-col--char { flex: none; }
.inv-col--main { flex: 1; min-width: 0; overflow-y: auto; }

/* 小标题 */
.sec-head { display: flex; align-items: center; gap: 7px; }
.sec-dot {
  width: 5px;
  height: 5px;
  flex: none;
  transform: rotate(45deg);
  background: #e0523b;
  box-shadow: 0 0 8px rgba(224, 82, 59, 0.7);
}
.sec-txt {
  font-family: 'LXGW WenKai', '霞鹜文楷', 'Kaiti SC', KaiTi, serif;
  font-size: 12px;
  letter-spacing: 0.28em;
  text-indent: 0.28em;
  color: #e2d4b0;
  white-space: nowrap;
}
.sec-meta {
  margin-left: auto;
  font-size: 9.5px;
  letter-spacing: 0.12em;
  color: rgba(233, 224, 204, 0.42);
  font-variant-numeric: tabular-nums;
}

/* ================= 角色与装备 ================= */
.doll {
  display: flex;
  align-items: stretch;
  gap: var(--sg);
}
.doll-col {
  display: flex;
  flex-direction: column;
  gap: var(--sg);
  justify-content: center;
}
.eslot {
  position: relative;
  width: var(--s);
  height: var(--s);
  display: grid;
  place-items: center;
  padding: 0;
  cursor: pointer;
  color: var(--paper-dim);
  clip-path: polygon(6px 0, 100% 0, 100% calc(100% - 6px), calc(100% - 6px) 100%, 0 100%, 0 6px);
  border: 2px solid rgba(200, 166, 89, 0.28);
  background: linear-gradient(180deg, #1b1814 0%, #110f0c 34%, #080706 70%, #050504 100%);
  box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.85);
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
.eslot::before {
  content: '';
  position: absolute;
  width: 7px;
  height: 7px;
  transform: rotate(45deg);
  border: 1px solid rgba(200, 166, 89, 0.22);
  transition: opacity 0.2s ease;
}
.eslot:hover { border-color: rgba(240, 214, 143, 0.5); box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.85), 0 0 14px rgba(200, 166, 89, 0.18); }
.eslot.has { border-color: rgba(200, 166, 89, 0.55); }
.eslot.has::before { opacity: 0; }
.eslot-ph {
  position: absolute;
  left: 4px;
  bottom: 2px;
  z-index: 3;
  font-family: 'LXGW WenKai', '霞鹜文楷', 'Kaiti SC', KaiTi, serif;
  font-size: 8px;
  letter-spacing: 0.06em;
  color: rgba(233, 224, 204, 0.3);
  pointer-events: none;
}
.eslot.has .eslot-ph { opacity: 0; }

/* 角色 */
.figure {
  position: relative;
  width: calc(var(--s) * 1.9);
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(200, 166, 89, 0.2);
  background:
    radial-gradient(70% 60% at 50% 22%, rgba(233, 224, 204, 0.07), transparent 70%),
    linear-gradient(180deg, rgba(30, 27, 21, 0.75), rgba(12, 11, 9, 0.9));
  clip-path: polygon(8px 0, 100% 0, 100% calc(100% - 8px), calc(100% - 8px) 100%, 0 100%, 0 8px);
  overflow: visible;
}
.figure.is-hurt .fig-char { filter: drop-shadow(0 0 8px rgba(179, 56, 42, 0.55)); }
.figure.is-hungry .fig-char { filter: saturate(0.5) brightness(0.85); }
.fig-char { width: 100%; height: calc(var(--s) * 3.6); display: flex; align-items: center; justify-content: center; }
.fig-char :deep(.char-svg) { height: 100%; width: auto; overflow: visible; }
.fig-char :deep(.ov) { pointer-events: none; }
.fig-badge {
  position: absolute;
  top: 3px;
  z-index: 4;
  display: flex;
  align-items: center;
  gap: 2px;
  padding: 1px 5px;
  font-size: 9px;
  font-variant-numeric: tabular-nums;
  clip-path: polygon(5px 0, 100% 0, 100% calc(100% - 5px), calc(100% - 5px) 100%, 0 100%, 0 5px);
  border: 1px solid rgba(200, 166, 89, 0.5);
  background: rgba(16, 14, 12, 0.85);
}
.fig-badge svg { width: 10px; height: 10px; }
.fig-badge svg * { fill: none; stroke: currentColor; stroke-width: 4; stroke-linecap: round; stroke-linejoin: round; }
.fig-badge--atk { left: 3px; color: #e4795f; }
.fig-badge--armor { right: 3px; color: #7fb99a; }
.fig-badge.off { opacity: 0.35; }
.fig-hp {
  position: absolute;
  left: 8%;
  right: 8%;
  bottom: 3px;
  height: 6px;
  overflow: hidden;
  border-radius: 2px 7px 7px 2px;
  background: linear-gradient(180deg, #1c1813, #080706);
  border: 1px solid rgba(200, 166, 89, 0.3);
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.85);
}
.fig-hp__fill {
  display: block;
  height: 100%;
  transition: width 0.25s ease;
  background: linear-gradient(180deg, #e97a60 0%, #cb4a36 30%, #a3321f 58%, #71200f 82%, #420f07 100%);
}
.fig-tag {
  position: absolute;
  right: 5px;
  bottom: 10px;
  font-family: 'LXGW WenKai', '霞鹜文楷', 'Kaiti SC', KaiTi, serif;
  font-size: 8px;
  letter-spacing: 0.16em;
  color: rgba(233, 224, 204, 0.38);
  pointer-events: none;
  writing-mode: vertical-rl;
}
.wep {
  position: absolute;
  z-index: 3;
  pointer-events: none;
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.9));
}
.wep svg { width: 100%; height: 100%; overflow: visible; }
.wep svg * { fill: none; stroke: currentColor; stroke-width: 3; stroke-linecap: round; stroke-linejoin: round; }
.wep--main { right: -12%; bottom: 22%; width: 56%; transform: rotate(-10deg); }
.wep--off { left: -12%; bottom: 22%; width: 50%; transform: rotate(10deg) scaleX(-1); }
.wep--amu { left: 50%; top: 30%; width: 34%; transform: translateX(-50%) rotate(-6deg); }

/* ================= 炼化 ================= */
.craft {
  display: flex;
  flex-direction: column;
  gap: 5px;
}
.craft-row {
  display: flex;
  align-items: center;
  gap: 8px;
}
.cgrid {
  display: grid;
  grid-template-columns: repeat(2, var(--s));
  grid-template-rows: repeat(2, var(--s));
  gap: var(--sg);
}
.craft-arrow {
  font-size: 16px;
  color: rgba(200, 166, 89, 0.7);
  text-shadow: 0 1px 2px #000;
}
.ccell--result { background: linear-gradient(180deg, #1f1b15, #0c0b09); }
.ccell--result.has { border-color: rgba(240, 214, 143, 0.65); box-shadow: 0 0 16px rgba(240, 214, 143, 0.25); }
.ccell-q {
  font-family: 'LXGW WenKai', '霞鹜文楷', 'Kaiti SC', KaiTi, serif;
  color: rgba(233, 224, 204, 0.25);
  font-size: 13px;
}

/* ================= 通用格子 ================= */
.cell {
  position: relative;
  width: var(--s);
  height: var(--s);
  padding: 0;
  cursor: pointer;
  color: var(--paper-dim);
  clip-path: polygon(6px 0, 100% 0, 100% calc(100% - 6px), calc(100% - 6px) 100%, 0 100%, 0 6px);
  border: 2px solid rgba(200, 166, 89, 0.16);
  background: linear-gradient(180deg, #171512 0%, #0e0d0b 40%, #070606 100%);
  box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.7);
  transition: border-color 0.18s ease, box-shadow 0.2s ease, transform 0.15s ease;
  animation: cellIn 0.34s cubic-bezier(0.2, 0.8, 0.25, 1) both;
  animation-delay: calc(var(--i, 0) * 10ms);
}
.cell::after {
  content: '';
  position: absolute;
  left: 50%;
  top: 50%;
  width: 8px;
  height: 8px;
  transform: translate(-50%, -50%) rotate(45deg);
  border: 1px solid rgba(200, 166, 89, 0.14);
  transition: opacity 0.2s ease;
}
.cell.has { cursor: grab; border-color: rgba(200, 166, 89, 0.34); }
.cell.has::after { opacity: 0; }
.cell.has:hover { transform: translateY(-1px); border-color: rgba(240, 214, 143, 0.62); box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.7), 0 4px 12px rgba(0, 0, 0, 0.7), 0 0 14px rgba(200, 166, 89, 0.2); }
.cell.is-sel {
  border-color: #f0d68f;
  box-shadow: 0 0 0 1px rgba(240, 214, 143, 0.45), 0 0 18px rgba(240, 214, 143, 0.3), inset 0 0 12px rgba(200, 166, 89, 0.16);
}
.cell.is-sel::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 4;
  background:
    linear-gradient(#e0523b, #e0523b) left 0 top 0 / 5px 2px no-repeat,
    linear-gradient(#e0523b, #e0523b) left 0 top 0 / 2px 5px no-repeat,
    linear-gradient(#e0523b, #e0523b) right 0 bottom 0 / 5px 2px no-repeat,
    linear-gradient(#e0523b, #e0523b) right 0 bottom 0 / 2px 5px no-repeat;
  opacity: 0.9;
}
.icon { position: absolute; inset: 10%; display: grid; place-items: center; pointer-events: none; z-index: 1; }
.icon svg { width: 84%; height: 84%; overflow: visible; filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.95)); }
.icon svg * { fill: none; stroke: currentColor; stroke-width: 2.1; stroke-linecap: round; stroke-linejoin: round; }
.r-common { color: #9d947f; }
.r-fine { color: #c3d3c6; }
.r-rare { color: #e4795f; }
.r-epic { color: #f0d68f; }
.cell.has.r-epic, .eslot.has.r-epic { border-color: rgba(240, 214, 143, 0.6); }
.cell.has.r-rare, .eslot.has.r-rare { border-color: rgba(224, 82, 59, 0.5); }
.qty {
  position: absolute;
  right: 2px;
  bottom: 1px;
  z-index: 3;
  min-width: 13px;
  padding: 0 2px;
  font-size: 8.5px;
  line-height: 1.4;
  font-variant-numeric: tabular-nums;
  text-align: center;
  color: #f6e9cd;
  background: linear-gradient(180deg, rgba(122, 51, 38, 0.95), rgba(44, 17, 12, 0.95));
  border: 1px solid rgba(214, 182, 116, 0.6);
  box-shadow: 0 1px 5px rgba(0, 0, 0, 0.8);
  pointer-events: none;
}

/* ================= 背包格阵 ================= */
.grid-wrap {
  display: flex;
  justify-content: center;
}
.grid {
  display: grid;
  grid-template-columns: repeat(9, var(--s));
  gap: var(--sg);
  justify-content: center;
}

/* ================= 状态模块 ================= */
.status {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4px 12px;
  padding: 7px 9px;
  border: 1px solid rgba(200, 166, 89, 0.24);
  background: linear-gradient(180deg, rgba(18, 16, 13, 0.72), rgba(9, 8, 7, 0.85));
  clip-path: polygon(8px 0, 100% 0, 100% calc(100% - 8px), calc(100% - 8px) 100%, 0 100%, 0 8px);
}
.stat { display: flex; align-items: center; gap: 6px; min-width: 0; }
.stat-ico { flex: none; width: 13px; height: 13px; }
.stat-ico svg { width: 100%; height: 100%; }
.stat-ico svg * { fill: none; stroke: currentColor; stroke-width: 3.4; stroke-linecap: round; stroke-linejoin: round; }
.stat-ico--hp { color: #e0523b; }
.stat-ico--food { color: #d8b569; }
.stat-ico--arm { color: #7fb99a; }
.stat-ico--xp { color: #9ac77f; }
.stat-name {
  flex: none;
  min-width: 2.6em;
  white-space: nowrap;
  font-family: 'LXGW WenKai', '霞鹜文楷', 'Kaiti SC', KaiTi, serif;
  font-size: 10px;
  letter-spacing: 0.14em;
  color: var(--paper-dim);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.9);
}
.stat-num {
  flex: none;
  min-width: 2.8em;
  text-align: right;
  white-space: nowrap;
  font-size: 8.5px;
  font-variant-numeric: tabular-nums;
  color: rgba(200, 166, 89, 0.9);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.9);
}
.bar {
  position: relative;
  flex: 1;
  min-width: 0;
  height: 9px;
  overflow: hidden;
  border-radius: 2px 8px 8px 2px;
  background: linear-gradient(180deg, #1c1813 0%, #110f0c 34%, #080706 72%, #050504 100%);
  border: 1px solid rgba(200, 166, 89, 0.22);
  box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.85);
}
.bar-lag, .bar-fill { position: absolute; left: 0; top: 0; bottom: 0; width: 0; }
.bar-lag {
  background: linear-gradient(180deg, rgba(233, 224, 204, 0.4), rgba(233, 224, 204, 0.08));
  transition: width 0.6s cubic-bezier(0.25, 0.8, 0.3, 1) 0.28s;
}
.bar-fill {
  transition: width 0.2s ease;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.4), inset 0 -2px 3px rgba(0, 0, 0, 0.55);
}
.bar--hp .bar-fill { background: linear-gradient(180deg, #e97a60 0%, #cb4a36 30%, #a3321f 58%, #71200f 82%, #420f07 100%); }
.bar--food .bar-fill { background: linear-gradient(180deg, #f7e6b4 0%, #d8b569 30%, #b08c3f 58%, #7d6023 82%, #48370f 100%); }
.bar--arm .bar-fill { background: linear-gradient(180deg, #a7cdb6 0%, #5d9179 30%, #3d6f5a 58%, #28503f 82%, #143026 100%); }
.bar--xp .bar-fill { background: linear-gradient(180deg, #bfe3a6 0%, #7fbf7f 30%, #4f9450 58%, #2c5a2c 82%, #123012 100%); }

/* ================= 详情 ================= */
.detail {
  display: grid;
  grid-template-columns: calc(var(--s) * 1.1) minmax(0, 1fr);
  gap: 8px;
  align-items: center;
  padding: 7px 9px;
  border: 1px solid rgba(200, 166, 89, 0.24);
  background:
    radial-gradient(80% 70% at 100% 0%, rgba(200, 166, 89, 0.06), transparent 68%),
    linear-gradient(180deg, rgba(18, 16, 13, 0.72), rgba(9, 8, 7, 0.85));
  clip-path: polygon(8px 0, 100% 0, 100% calc(100% - 8px), calc(100% - 8px) 100%, 0 100%, 0 8px);
}
.detail-preview {
  position: relative;
  aspect-ratio: 1 / 1;
  clip-path: polygon(7px 0, 100% 0, 100% calc(100% - 7px), calc(100% - 7px) 100%, 0 100%, 0 7px);
  border: 2px solid rgba(200, 166, 89, 0.4);
  background: linear-gradient(180deg, #1d1a15, #0b0a08);
  box-shadow: inset 0 0 16px rgba(0, 0, 0, 0.85);
}
.detail-info { min-width: 0; display: flex; flex-direction: column; gap: 3px; }
.detail-name {
  margin: 0;
  font-family: 'LXGW WenKai', '霞鹜文楷', 'Kaiti SC', KaiTi, serif;
  font-size: 12.5px;
  letter-spacing: 0.1em;
  color: #f2e6c9;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.95);
  display: flex;
  align-items: baseline;
  gap: 6px;
  flex-wrap: wrap;
}
.detail-rarity { font-size: 8.5px; letter-spacing: 0.18em; font-family: serif; }
.detail-rarity.r-epic { color: #f0d68f; }
.detail-rarity.r-rare { color: #e0523b; }
.detail-rarity.r-fine { color: #c3d3c6; }
.detail-rarity.r-common { color: #9d947f; }
.detail-qty { font-size: 9px; color: rgba(233, 224, 204, 0.55); }
.detail-type {
  font-size: 9px;
  letter-spacing: 0.1em;
  color: rgba(233, 224, 204, 0.55);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.detail-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(64px, 1fr));
  gap: 1px 10px;
}
.detail-stat-row { display: flex; justify-content: space-between; gap: 6px; font-size: 9px; }
.detail-stat-row span { color: rgba(233, 224, 204, 0.6); }
.detail-stat-row b { color: #f0d68f; font-weight: 600; font-variant-numeric: tabular-nums; }
.detail-acts { display: flex; gap: 5px; flex-wrap: wrap; margin-top: 2px; }
.dbtn {
  position: relative;
  padding: 3px 10px;
  cursor: pointer;
  font-family: 'LXGW WenKai', '霞鹜文楷', 'Kaiti SC', KaiTi, serif;
  font-size: 10px;
  letter-spacing: 0.2em;
  text-indent: 0.2em;
  color: rgba(233, 224, 204, 0.78);
  clip-path: polygon(6px 0, 100% 0, 100% calc(100% - 6px), calc(100% - 6px) 100%, 0 100%, 0 6px);
  border: 2px solid transparent;
  background:
    linear-gradient(180deg, rgba(38, 33, 26, 0.82), rgba(16, 14, 12, 0.88)) padding-box,
    repeating-linear-gradient(58deg, rgba(255, 242, 210, 0.16) 0 1px, transparent 1px 4px) border-box,
    linear-gradient(140deg, rgba(240, 214, 143, 0.8), rgba(122, 98, 52, 0.4) 52%, rgba(240, 214, 143, 0.7)) border-box;
}
.dbtn:hover { color: #f6ecd2; box-shadow: 0 0 16px rgba(200, 166, 89, 0.3); }
.dbtn--ghost {
  color: rgba(233, 224, 204, 0.55);
  background:
    linear-gradient(180deg, rgba(24, 21, 17, 0.7), rgba(12, 11, 9, 0.8)) padding-box,
    linear-gradient(140deg, rgba(200, 166, 89, 0.5), rgba(122, 98, 52, 0.28) 52%, rgba(200, 166, 89, 0.45)) border-box;
}
.detail-empty {
  margin: 0;
  padding: 8px;
  text-align: center;
  font-family: 'LXGW WenKai', '霞鹜文楷', 'Kaiti SC', KaiTi, serif;
  font-size: 11px;
  letter-spacing: 0.24em;
  color: rgba(233, 224, 204, 0.3);
  border: 1px solid rgba(200, 166, 89, 0.18);
  clip-path: polygon(8px 0, 100% 0, 100% calc(100% - 8px), calc(100% - 8px) 100%, 0 100%, 0 8px);
}

/* ================= 底栏 ================= */
.inv-foot {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
  padding-top: 6px;
  border-top: 1px solid rgba(200, 166, 89, 0.22);
  font-size: 9.5px;
  letter-spacing: 0.1em;
  color: rgba(233, 224, 204, 0.52);
}
.foot-meter b { color: #c8a659; font-weight: 600; font-variant-numeric: tabular-nums; }
.foot-hints { margin-left: auto; }
.foot-hints b { color: #f0d68f; font-weight: 600; padding: 0 3px; border: 1px solid rgba(200, 166, 89, 0.45); background: rgba(200, 166, 89, 0.1); font-size: 0.92em; }

/* ================= 浮签 ================= */
.tip {
  position: fixed;
  left: 0;
  top: 0;
  z-index: 9999;
  width: min(230px, 72vw);
  padding: 8px 10px;
  pointer-events: none;
  clip-path: polygon(8px 0, 100% 0, 100% calc(100% - 8px), calc(100% - 8px) 100%, 0 100%, 0 8px);
  border: 2px solid transparent;
  background:
    linear-gradient(180deg, rgba(30, 26, 20, 0.97), rgba(12, 11, 9, 0.97)) padding-box,
    repeating-linear-gradient(58deg, rgba(255, 242, 210, 0.18) 0 1px, transparent 1px 4px) border-box,
    linear-gradient(140deg, rgba(240, 214, 143, 0.85), rgba(122, 98, 52, 0.42) 52%, rgba(240, 214, 143, 0.7)) border-box;
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.72);
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.14s ease, visibility 0.14s ease;
}
.tip-name {
  margin: 0 0 4px;
  font-family: 'LXGW WenKai', '霞鹜文楷', 'Kaiti SC', KaiTi, serif;
  font-size: 12px;
  letter-spacing: 0.1em;
  color: #f2e6c9;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.95);
  display: flex;
  align-items: baseline;
  gap: 6px;
  flex-wrap: wrap;
}
.tip-rarity { font-size: 8.5px; letter-spacing: 0.18em; }
.tip-rarity.r-epic { color: #f0d68f; }
.tip-rarity.r-rare { color: #e0523b; }
.tip-rarity.r-fine { color: #c3d3c6; }
.tip-rarity.r-common { color: #9d947f; }
.tip-type {
  margin: 0 0 4px;
  font-size: 9px;
  letter-spacing: 0.1em;
  color: rgba(233, 224, 204, 0.5);
}
.tip-stats {
  display: grid;
  gap: 2px;
  margin-bottom: 4px;
}
.tip-stats div {
  display: flex;
  justify-content: space-between;
  gap: 8px;
  font-size: 9.5px;
  color: rgba(233, 224, 204, 0.62);
  letter-spacing: 0.08em;
}
.tip-stats b { color: #f0d68f; font-weight: 600; font-variant-numeric: tabular-nums; }
.tip-flavor {
  margin: 0;
  padding-left: 7px;
  border-left: 1px solid rgba(200, 166, 89, 0.3);
  font-size: 9px;
  line-height: 1.6;
  color: rgba(233, 224, 204, 0.46);
}

/* ================= 提示语 ================= */
.toast {
  position: fixed;
  left: 50%;
  bottom: 20px;
  transform: translate(-50%, 10px);
  padding: 5px 15px;
  z-index: 10000;
  font-family: 'LXGW WenKai', '霞鹜文楷', 'Kaiti SC', KaiTi, serif;
  font-size: 12px;
  letter-spacing: 0.2em;
  color: #efdfba;
  white-space: nowrap;
  clip-path: polygon(8px 0, 100% 0, 100% calc(100% - 8px), calc(100% - 8px) 100%, 0 100%, 0 8px);
  border: 2px solid transparent;
  background:
    linear-gradient(180deg, rgba(40, 34, 26, 0.9), rgba(18, 16, 13, 0.86)) padding-box,
    repeating-linear-gradient(58deg, rgba(255, 242, 210, 0.18) 0 1px, transparent 1px 4px) border-box,
    linear-gradient(140deg, rgba(240, 214, 143, 0.85), rgba(122, 98, 52, 0.42) 50%, rgba(240, 214, 143, 0.7)) border-box;
  box-shadow: 0 8px 22px rgba(0, 0, 0, 0.55);
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s ease, transform 0.3s ease;
}
.toast.is-on { opacity: 1; transform: translate(-50%, 0); }

/* ================= 丢弃指示 ================= */
.discard {
  position: fixed;
  left: 0;
  top: 0;
  z-index: 10001;
  width: 52px;
  height: 52px;
  display: grid;
  place-items: center;
  border-radius: 50%;
  font-family: 'LXGW WenKai', '霞鹜文楷', 'Kaiti SC', KaiTi, serif;
  font-size: 15px;
  letter-spacing: 0.1em;
  color: #ffe6d8;
  border: 2px solid rgba(255, 210, 180, 0.6);
  background: radial-gradient(circle at 35% 30%, rgba(224, 82, 59, 0.95), rgba(122, 20, 10, 0.92));
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.7), 0 0 18px rgba(179, 56, 42, 0.6);
  pointer-events: none;
  opacity: 0;
  transform: translate(-50%, -50%) scale(0.7);
  transition: opacity 0.16s ease, transform 0.16s ease;
}
.discard.is-on { opacity: 1; transform: translate(-50%, -50%) scale(1); }

.svgdefs { position: absolute; width: 0; height: 0; overflow: hidden; pointer-events: none; }

@keyframes cellIn {
  0% { opacity: 0; transform: translateY(5px) scale(0.95); }
  100% { opacity: 1; transform: none; }
}

@media (max-width: 560px) {
  .inv-body { flex-direction: column; }
  .inv-col--char { flex-direction: row; align-items: flex-start; }
  .inv-col--main { overflow: visible; }
}
</style>
