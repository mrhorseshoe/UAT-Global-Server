<template>
  <div id="support-card-select-modal" class="modal fade" data-backdrop="static" data-keyboard="false">
    <div class="modal-dialog modal-dialog-centered modal-xl">
      <div class="modal-content" @click.stop>
        <div class="modal-header d-flex align-items-center justify-content-between">
          <h5 class="mb-0">Borrowing Support Card</h5>
          <div>
            <button class="btn btn-sm btn-outline-secondary me-2" @click="handleCancel">Cancel</button>
            <button class="btn btn-sm btn--primary" @click="handleConfirm" :disabled="isConfirmDisabled">Confirm</button>
          </div>
        </div>
        <div class="modal-body support-card-modal-body">
          <div class="section-card p-3 mb-2">
          <div class="type-btn-row">
            <button
              v-for="type in supportCardTypes"
              :key="type.name"
              type="button"
              class="type-btn"
              :class="[ { active: activeType === type.name }, type.name === 'custom' ? 'custom-btn' : '' ]"
              @click="setActiveType(type.name)"
              >
              <span class="type-btn-text">{{ type.label }}</span>
            </button>
          </div>
          <hr class="type-btn-divider"/>
          <div v-if="activeType !== 'custom'" class="support-card-list mt-3">
            <div
              v-for="card in filteredSupportCardList"
              :key="card.id"
              class="support-card-row"
              :class="{ 'selected-card': selectedCard && selectedCard.id === card.id }"
              @click="selectCard(card)"
            >
              <span class="card-rarity" :class="'rarity-' + card.rarity.toLowerCase()">{{ card.rarity }}</span>
              <span class="card-name">{{ card.name }}</span>
              <span class="card-chara">{{ card.desc }}</span>
            </div>
          </div>
          <div v-if="activeType === 'custom'" class="mt-3">
            <input type="text" class="form-control" placeholder="Enter card name here example 'Planned Perfection' or 'Fire at My Heels'" v-model="customCardName">
          </div>
          </div>
        </div>
        <div class="modal-footer d-none"></div>
      </div>
    </div>
  </div>
</template>

<script>
// Exported from the game's master.mdb (support_card_data + text_data)
import supportCards from '../assets/support_cards.json';

export default {
  name: "SupportCardSelectModal",
  props: {
    show: {
      type: Boolean,
      required: true
    }
  },
  emits: ['update:show', 'cancel', 'confirm'],
  data() {
    return {
      umamusumeSupportCardList: supportCards,
      selectedCard: null,
      customCardName: '',
      supportCardTypes: [
        { name: 'speed', label: 'Speed' },
        { name: 'stamina', label: 'Stamina' },
        { name: 'power', label: 'Power' },
        { name: 'guts', label: 'Guts' },
        { name: 'wit', label: 'Wit' },
        { name: 'friend', label: 'Friend' },
        { name: 'group', label: 'Group' },
        { name: 'custom', label: 'Custom' }
      ],
      activeType: 'speed',
    }
  },
  computed: {
    isConfirmDisabled() {
      return this.activeType === 'custom' && !this.customCardName.trim();
    },
    filteredSupportCardList() {
      if (this.activeType === 'custom') return [];
      return this.umamusumeSupportCardList.filter(card => card.type === this.activeType);
    },
  },
  watch: {
    show(newVal) {
      if (newVal) {
        // 显示弹窗
        $('#support-card-select-modal').modal({
          backdrop: 'static',
          keyboard: false,
          show: true
        });
        // 默认选中第一个
        if (!this.selectedCard) {
          this.selectedCard = this.filteredSupportCardList[0];
        }
      } else {
        // 隐藏弹窗
        $('#support-card-select-modal').modal('hide');
      }
    }
  },
  methods: {
    handleCancel() {
      this.$emit('update:show', false);
      this.$emit('cancel');
      // 恢复父modal滚动
      this.$nextTick(() => {
        this.restoreParentModalScrolling();
      });
    },
    handleConfirm() {
      if (this.activeType === 'custom') {
        this.$emit('confirm', { name: this.customCardName, id: 'custom' });
      } else {
        this.$emit('confirm', this.selectedCard);
      }
      this.$emit('update:show', false);
      // 恢复父modal滚动
      this.$nextTick(() => {
        this.restoreParentModalScrolling();
      });
    },
    restoreParentModalScrolling() {
      setTimeout(() => {
        if ($('.modal-open').length > 0) {
          $('body').addClass('modal-open');
          const parentModal = $('#create-task-list-modal');
          if (parentModal.hasClass('show')) {
            const modalBody = parentModal.find('.modal-body');
            if (modalBody.length > 0) {
              modalBody.css('overflow-y', 'auto');
              modalBody[0].offsetHeight;
            }
          }
        }
      }, 100);
    },
    setActiveType(type) {
      this.activeType = type;
      if (type !== 'custom') {
        this.selectCard(this.filteredSupportCardList[0]);
      }
    },
    selectCard(card) {
      this.selectedCard = card;
    },
  },
  mounted() {
    $('#support-card-select-modal').on('hidden.bs.modal', () => {
      this.$emit('update:show', false);
      this.$nextTick(() => {
        this.restoreParentModalScrolling();
      });
    });
  }
}
</script>

<style scoped>
.cancel-btn {
  background-color: #dc3545 !important;
  color: white !important;
  padding: 0.4rem 0.8rem !important;
  font-size: 1rem !important;
  border-radius: 0.25rem;
  border: none;
  cursor: pointer;
  min-width: 60px;
  min-height: 30px;
  font-weight: 500;
}
.cancel-btn:hover {
  background-color: #c82333 !important;
  color: white !important;
}
.auto-btn {
  background-color: var(--accent) !important;
  color: #fff !important;
  padding: 0.4rem 0.8rem !important;
  font-size: 1rem !important;
  border-radius: 0.25rem;
  border: none;
  cursor: pointer;
  min-width: 60px;
  min-height: 30px;
  font-weight: 500;
}
.auto-btn:hover {
  background-color: var(--accent-2) !important;
  color: #fff !important;
}
/* 保证弹窗在遮罩层之上 */
#support-card-select-modal.modal {
  z-index: 1060;
}
#support-card-select-modal .modal-dialog {
  z-index: 1061;
}
.section-card{border:1px solid var(--accent);border-radius:12px;box-shadow:none} 
.support-card-modal-body {
  max-height: 600px;
  overflow-y: auto;
  /* 让footer固定时，body不被footer遮挡 */
  padding-bottom: 80px;
}
.support-card-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.support-card-row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 10px;
  border: 1px solid rgba(255,255,255,.12);
  border-radius: 8px;
  cursor: pointer;
}
.support-card-row:hover {
  border-color: var(--accent);
  background: rgba(255,45,163,.08);
}
.support-card-row.selected-card {
  border-color: var(--accent);
  background: rgba(255,45,163,.16);
  box-shadow: 0 0 0 1px var(--accent) inset;
}
.card-rarity {
  flex: 0 0 42px;
  text-align: center;
  font-weight: 700;
  font-size: .8rem;
  border: 1px solid #9aa;
  border-radius: 6px;
  color: #9aa;
}
.card-rarity.rarity-ssr { color: #ffd700; border-color: #ffd700; }
.card-rarity.rarity-sr { color: #ffa64d; border-color: #ffa64d; }
.card-name {
  font-weight: 600;
  color: #fff;
}
.card-chara {
  margin-left: auto;
  color: #bbb;
  font-size: .9rem;
}
.type-btn-row {
  display: flex;
  justify-content: flex-start; /* 靠左对齐 */
  align-items: center;
  gap: 8px;
  margin-top: 12px;
  margin-bottom: 8px;
}
.type-btn {
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
  outline: none;
  width: auto;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}
/* Allow custom button to size to its text to avoid overlap with neighbors */
.type-btn.custom-btn {
  width: auto;
  height: 40px;
}
/* remove data-text pseudo label to avoid duplicate text */
/* Custom tab text appearance */
.type-btn-text {
  color: hotpink;
  font-size: 14px;
  line-height: 32px;
  padding: 0 10px;
  border: 2px solid hotpink;
  border-radius: 8px;
}
/* When inactive, keep transparent background with pink border and pink text */
.type-btn.custom-btn:not(.active) .type-btn-text {
  background: transparent;
  color: hotpink;
}
/* When active, solid pink with black text */
.type-btn.custom-btn.active .type-btn-text {
  background: hotpink;
  color: #000;
}
/* Remove default active background/border for the custom container to avoid double borders */
.type-btn.custom-btn.active {
  background: transparent;
  border-color: transparent;
}
.type-btn-divider {
  border: none;
  border-top: 1px solid var(--accent);
  margin: 0 0 12px 0;
}
.type-btn.active {
  border: 2px solid var(--accent);
  border-radius: 8px;
  background: rgba(255,64,129,.12);
}
/* Keep custom inactive button container without default border so only text pill shows border */
.type-btn.custom-btn:not(.active) {
  border: none;
}
</style>
