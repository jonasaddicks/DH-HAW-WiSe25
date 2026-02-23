<script>
export default {
  props: {
    visible: Boolean
  },
  emits: [
    "confirm",
    "cancel"
  ],
};
</script>

<template>
        <!-- Auswahl bestätigen Popup-->
    <div v-if="visible" class="confirmation-popup"><div class="confirmation-popup-buttons">
        <p>Route berechnen?</p>
        <button @click="$emit('cancel')">Abbrechen</button>
        <button @click="$emit('confirm')">Bestätigen</button>
        </div>
    </div>
</template>

<style scoped>
  .confirmation-popup {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  width: 80%;
  background: white;
  border-radius: 10px;
  padding: 16px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.2);
  z-index: 1000;
}

.confirmation-popup p {
  margin: 0 0 10px 0;
  font-size: 14px;
}

.confirmation-popup-buttons {
  display: flex;
  gap: 8px;
  margin-top: 10px;
  justify-content: flex-end;
}

.confirmation-popup-buttons button {
  padding: 8px 16px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-size: 14px;
}

.confirmation-popup-buttons button:last-child {
  background: var(--color-accent);
  color: white;
}
</style>