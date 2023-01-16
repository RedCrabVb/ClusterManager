import { Component, Input } from '@angular/core';

@Component({
    selector: 'app-header',
    templateUrl: './initfile.component.html',
})

export class InitFileComponent {
    @Input() title: string;
}