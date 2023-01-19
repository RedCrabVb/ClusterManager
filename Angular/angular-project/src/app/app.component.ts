import { Component, Input } from '@angular/core';
import { product as data } from './date/product';
import { ProductsService } from './services/Products.service'; 
import { InitFileService } from './services/initfile.service'; 

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'angular-project';
  products = data

  constructor(private productsService: ProductsService, private initFileService: InitFileService) {

  }

  sendInitFile() {
    console.log('Click me!')
    this.initFileService.get().subscribe((res) => {console.log(res)});
    this.initFileService.uploadFile('bla-bla', '0101010', 'hadoop-test-user-name').subscribe((res) => {console.log(res)})
  }
}
