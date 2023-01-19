import { Component, Input } from '@angular/core';
import { InitFile as data } from '../../date/initfile';
import { ProductsService } from '../../services/Products.service';
import { InitFileService } from '../../services/initfile.service';
import { ModalService } from 'src/app/components/modal/modalService';
import { IInitFile } from 'src/app/date/IInitfile';
// import { ConsoleReporter } from 'jasmine';

@Component({
  selector: 'app-initfile',
  templateUrl: './initfile.page.component.html',
  styleUrls: ['./initfile.page.component.css']
})
export class InitFilePage {
  title = 'angular-project';
  products = data

  nameuser = ''
  namefile: string = ''
  fileToUpload: File;

  constructor(private productsService: ProductsService, private initFileService: InitFileService, private modalService: ModalService) {
    this.initFileService.getAllInitfiles().subscribe((initfiles: any) => {
      console.log(initfiles);
      this.products = initfiles
    })
  }

  updateNameUser(event: any) {
    console.log(this.nameuser)
    console.log(event)
    this.nameuser = event.target.value
  }

  sendInitFile() {
    const reader = new FileReader();

    reader.readAsDataURL(this.fileToUpload);
    reader.onload = () => {
        console.log(reader.result);
        if (reader.result != undefined) {
          this.initFileService.uploadFile(this.namefile, reader.result.toString(), this.nameuser).subscribe((res) => {console.log(res); alert("success upload!")})
        }
    };

    this.initFileService.getAllInitfiles().subscribe((initfiles: any) => {
      console.log(initfiles);
      this.products = initfiles
    })
  }

  handleFileInput(event: Event) {
    var tmpFile = (event.currentTarget as HTMLInputElement).files?.item(0);
    if (tmpFile != undefined) {
      this.fileToUpload = tmpFile;
      this.namefile = this.fileToUpload.name;
    }
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
