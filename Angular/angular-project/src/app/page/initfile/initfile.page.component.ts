import { Component, Input } from '@angular/core';
import { InitFile as data } from '../../date/initfile';
import { ProductsService } from '../../services/Products.service'; 
import { InitFileService } from '../../services/initfile.service'; 
import { ModalService } from 'src/app/components/modal/modalService';

@Component({
  selector: 'app-initfile',
  templateUrl: './initfile.page.component.html',
  // styleUrls: ['./app.component.css']
})
export class InitFilePage {
  title = 'angular-project';
  products = data
  nameuser = ''  

  constructor(private productsService: ProductsService, private initFileService: InitFileService, private modalService: ModalService) {

  }

  sendInitFile(event: any) {
    console.log(this.nameuser)
    console.log(event)
    this.nameuser = event.target.value
  }

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
