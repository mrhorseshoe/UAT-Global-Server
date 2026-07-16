<template>
  <div id="spark-reroll-modal" class="modal fade" data-backdrop="static" data-keyboard="false">
    <div class="modal-dialog modal-dialog-centered modal-lg">
      <div class="modal-content" @click.stop>
        <div class="modal-header d-flex align-items-center justify-content-between">
          <h5 class="mb-0">Spark Reroll Options</h5>
          <div>
            <button class="btn btn-sm btn-outline-secondary me-2" @click="cancel">Cancel</button>
            <button class="btn btn-sm btn--primary" @click="confirm">Confirm</button>
          </div>
        </div>
        <div class="modal-body">
          <p class="text-muted">
            At the end-of-career spark screen the bot keeps the roll if any checked spark appears
            at or above the minimum stars. Otherwise it rerolls once (30 TP) and picks the rerolled
            set if it satisfies the check; if neither set does, it keeps the set with the most white sparks.
          </p>

          <!-- Blue stat sparks -->
          <div class="form-group section-card p-3 mb-3">
            <h6 class="mb-2">Blue Sparks (Stats)</h6>
            <div class="d-flex flex-wrap">
              <div class="form-check mr-4" v-for="name in blueSparks" :key="name">
                <input type="checkbox" class="form-check-input" :id="'spark-' + idFor(name)"
                  :value="name" v-model="internalTargets">
                <label class="form-check-label" :for="'spark-' + idFor(name)">{{ name }}</label>
              </div>
            </div>
          </div>

          <!-- Pink aptitude sparks -->
          <div class="form-group section-card p-3 mb-3">
            <h6 class="mb-2">Pink Sparks (Aptitudes)</h6>
            <div class="row">
              <div class="col-md-3 col-6" v-for="group in pinkGroups" :key="group.label">
                <div class="pink-group-label">{{ group.label }}</div>
                <div class="form-check" v-for="name in group.sparks" :key="name">
                  <input type="checkbox" class="form-check-input" :id="'spark-' + idFor(name)"
                    :value="name" v-model="internalTargets">
                  <label class="form-check-label" :for="'spark-' + idFor(name)">{{ name }}</label>
                </div>
              </div>
            </div>
          </div>

          <!-- Minimum stars -->
          <div class="form-group section-card p-3 mb-3">
            <h6 class="mb-2">Minimum Stars</h6>
            <p class="text-muted mb-2">A checked spark only counts as a hit at this star level or higher.</p>
            <select v-model.number="internalMinStars" class="form-control" style="max-width: 200px;"
              id="spark-reroll-min-stars">
              <option :value="1">1 star</option>
              <option :value="2">2 stars</option>
              <option :value="3">3 stars</option>
            </select>
          </div>

          <!-- Carat usage when TP is short -->
          <div class="form-group section-card p-3">
            <h6 class="mb-2">Insufficient TP</h6>
            <div class="form-check">
              <input type="checkbox" class="form-check-input" id="spark-reroll-use-carats"
                v-model="internalUseCarats">
              <label class="form-check-label" for="spark-reroll-use-carats">
                Spend carats to restore TP when a reroll can't be afforded
              </label>
            </div>
            <p class="text-muted mb-0 mt-1">
              A reroll costs 30 TP. If the career ends with too little TP, the bot restores it
              (using a TP item first if you have one, otherwise carats) and rerolls. When unchecked,
              it keeps the original sparks instead.
            </p>
          </div>
        </div>
        <div class="modal-footer d-none"></div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SparkRerollModal',
  props: {
    show: Boolean,
    targets: {
      type: Array,
      default: () => []
    },
    minStars: {
      type: Number,
      default: 3
    },
    useCarats: {
      type: Boolean,
      default: false
    },
  },
  emits: ['update:show', 'confirm', 'cancel'],
  data() {
    return {
      blueSparks: ['Speed', 'Stamina', 'Power', 'Guts', 'Wit'],
      pinkGroups: [
        { label: 'Track', sparks: ['Turf', 'Dirt'] },
        { label: 'Distance', sparks: ['Sprint', 'Mile', 'Medium', 'Long'] },
        { label: 'Style', sparks: ['Front Runner', 'Pace Chaser', 'Late Surger', 'End Closer'] },
      ],
      internalTargets: [...this.targets],
      internalMinStars: this.minStars,
      internalUseCarats: this.useCarats,
    };
  },
  watch: {
    show(newVal) {
      if (newVal) {
        $('#spark-reroll-modal').modal({
          backdrop: 'static',
          keyboard: false,
          show: true
        });
      } else {
        $('#spark-reroll-modal').modal('hide');
      }
    },
    targets: {
      handler(newVal) {
        this.internalTargets = [...newVal];
      },
      deep: true
    },
    minStars(newVal) {
      this.internalMinStars = newVal;
    },
    useCarats(newVal) {
      this.internalUseCarats = newVal;
    },
  },
  methods: {
    idFor(name) {
      return name.toLowerCase().replace(/\s+/g, '-');
    },
    confirm() {
      this.$emit('confirm', {
        targets: [...this.internalTargets],
        minStars: Number(this.internalMinStars),
        useCarats: Boolean(this.internalUseCarats),
      });
      this.$emit('update:show', false);
      this.$nextTick(() => {
        this.restoreParentModalScrolling();
      });
    },
    cancel() {
      this.$emit('update:show', false);
      this.$emit('cancel');
      this.$nextTick(() => {
        this.restoreParentModalScrolling();
      });
    },
    restoreParentModalScrolling() {
      // Restore parent modal scroll function
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
  },
  mounted() {
    $('#spark-reroll-modal').on('hidden.bs.modal', () => {
      this.$emit('update:show', false);
      this.$nextTick(() => {
        this.restoreParentModalScrolling();
      });
    });
  }
};
</script>

<style scoped>
#spark-reroll-modal.modal {
  z-index: 1060;
}

#spark-reroll-modal .modal-dialog {
  z-index: 1061;
}

.section-card {
  border: 1px solid var(--accent);
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, .06);
}

.pink-group-label {
  font-weight: 600;
  margin-bottom: 4px;
}
</style>
