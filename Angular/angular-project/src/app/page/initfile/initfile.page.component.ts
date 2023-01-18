import { Component, Input } from '@angular/core';
import { InitFile as data } from '../../date/initfile';
import { ProductsService } from '../../services/Products.service'; 
import { InitFileService } from '../../services/initfile.service'; 

@Component({
  selector: 'app-initfile',
  templateUrl: './initfile.page.component.html',
  // styleUrls: ['./app.component.css']
})
export class InitFilePage {
  title = 'angular-project';
  products = data

  constructor(private productsService: ProductsService, private initFileService: InitFileService) {

  }

  sendInitFile() {

  }
}
