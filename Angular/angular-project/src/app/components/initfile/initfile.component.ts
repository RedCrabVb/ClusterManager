import { Component, Input } from '@angular/core';
import { IInitFile } from 'src/app/date/IInitfile';
import { ModalService } from './initfile.modalService';

@Component({
    selector: 'item-initfile',
    templateUrl: './initfile.component.html',
})

export class InitFileComponent {
    @Input() initfile: IInitFile;

    constructor(private modalService: ModalService) { }

    ngOnInit() {
        // this.bodyText = 'This text can be updated in modal 1';
    }

    openModal(id: string) {
        this.modalService.open(id);
    }

    closeModal(id: string) {
        this.modalService.close(id);
    }
}