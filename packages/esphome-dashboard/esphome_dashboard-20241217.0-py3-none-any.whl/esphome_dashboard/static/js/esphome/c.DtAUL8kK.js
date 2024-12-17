import{H as o,b as t,c as s,k as e,n as i,s as r,x as n,J as a}from"./index-D-cxILmb.js";import"./c.Bu6MtT5R.js";import{o as l}from"./c.DQX3ggiU.js";import"./c.CyiVjy7U.js";import"./c.CV6cyzYS.js";import"./c.CBPI5kTQ.js";let c=class extends r{render(){return n`
      <esphome-process-dialog
        always-show-close
        .heading=${`Logs ${this.configuration}`}
        .type=${"logs"}
        .spawnParams=${{configuration:this.configuration,port:this.target}}
        @closed=${this._handleClose}
        @process-done=${this._handleProcessDone}
      >
        <mwc-button
          slot="secondaryAction"
          dialogAction="close"
          label="Edit"
          @click=${this._openEdit}
        ></mwc-button>
        ${void 0===this._result||0===this._result?"":n`
              <mwc-button
                slot="secondaryAction"
                dialogAction="close"
                label="Retry"
                @click=${this._handleRetry}
              ></mwc-button>
            `}
      </esphome-process-dialog>
    `}_openEdit(){a(this.configuration)}_handleProcessDone(o){this._result=o.detail}_handleRetry(){l(this.configuration,this.target)}_handleClose(){this.parentNode.removeChild(this)}};c.styles=[o],t([s()],c.prototype,"configuration",void 0),t([s()],c.prototype,"target",void 0),t([e()],c.prototype,"_result",void 0),c=t([i("esphome-logs-dialog")],c);
//# sourceMappingURL=c.DtAUL8kK.js.map
