import { Component, Input } from '@angular/core';
import { IInitFile } from 'src/app/date/IInitfile';

@Component({
    selector: 'item-initfile',
    templateUrl: './initfile.component.html',
})

export class InitFileComponent {
    @Input() initfile: IInitFile;
}