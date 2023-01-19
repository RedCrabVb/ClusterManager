import { Component, Input } from '@angular/core';
import { IInitFile } from 'src/app/date/IInitfile';
import { ModalService } from '../modal/modalService';

@Component({
    selector: 'item-initfile',
    templateUrl: './initfile.component.html',
})

export class InitFileComponent {
    @Input() initfile: IInitFile;


}