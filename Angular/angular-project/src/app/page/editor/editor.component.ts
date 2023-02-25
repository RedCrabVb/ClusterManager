import { Component } from '@angular/core';
 
@Component({
  selector: 'my-component-ace',
  template: `
  <div ace-editor
       [(text)]="text" 
       ></div>
  `
})
export class MyComponent {
    text:string = "";
}