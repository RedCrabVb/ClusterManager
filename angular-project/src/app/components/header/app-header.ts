import { Component, Input } from '@angular/core';

@Component({
    selector: 'app-header',
    templateUrl: './app-header.html',
})

export class AppHeaderComponent {
    public isCollapsed = true;
}