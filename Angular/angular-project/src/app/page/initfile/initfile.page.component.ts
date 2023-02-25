import { Component, OnInit } from '@angular/core';
import { InitFile as data } from '../../date/initfile';
import { InitFileService } from '../../services/initfile.service';
import { ModalService } from 'src/app/components/modal/modalService';
import { IInitFile } from 'src/app/date/IInitfile';
import { HttpErrorResponse } from '@angular/common/http';
import { catchError, throwError } from 'rxjs';

@Component({
  selector: 'app-initfile',
  templateUrl: './initfile.page.component.html',
  styleUrls: ['./initfile.page.component.css']
})
export class InitFilePage implements OnInit {
  initfiles = data

  nameuser = ''
  namefile: string = ''
  fileToUpload: File;

  currentItemInitFile: IInitFile

  constructor(private initFileService: InitFileService, private modalService: ModalService) {

  }

  
  private handleError(error: HttpErrorResponse) {
    if (error.status === 0) {
      console.error('An error occurred:', error.error);
      alert('An error occurred: ' + error.message);
    } else {
      console.error(
        `Backend returned code ${error.status}, body was: `, error.error);

      alert(`Backend returned code ${error.status}, body was: ` + error.message);
    }
    return throwError(() => new Error('Something bad happened; please try again later.'));
  }

  ngOnInit(): void {
    this.updateInitFile();
  }

  updateInitFile() {
    this.initFileService.getAllInitfiles()
    .pipe(catchError(this.handleError))
    .subscribe((initfiles: any) => {
      console.log(initfiles);
      this.initfiles = initfiles
    })
  }

  openLicenseText(item: IInitFile) {
    this.currentItemInitFile = item;
    this.openModal('custom-modal-2');
  }

  acceptLicense() {
    this.initFileService.acceptLicense(this.currentItemInitFile.name, this.currentItemInitFile.version)
    .pipe(catchError(this.handleError))
    .subscribe((initfiles: any) => {
      console.log(initfiles);
      this.updateInitFile();
    });
  }

  deleteInitFile(name: string, version: string) {
    this.initFileService.deleteFile(name, version)
      .pipe(catchError(this.handleError))
      .subscribe((res: any) => { 
        console.log(res);
        this.updateInitFile();
        this.closeModal('custom-modal-2');
       });
  }

  updateNameUser(event: any) {
    this.nameuser = event.target.value;
  }

  sendInitFile() {
    const reader = new FileReader();
    if (this.fileToUpload == null) {
      alert('Not found file');
      return;
    }
    reader.readAsDataURL(this.fileToUpload);
    reader.onload = () => {
      console.log(reader.result);
      if (reader.result != undefined) {
        this.initFileService.uploadFile(this.namefile, reader.result.toString(), this.nameuser)
          .pipe(catchError(this.handleError))
          .subscribe((res) => {
            console.log(res); 
            this.updateInitFile();
            alert("success upload!");
          })
      }
    };


  }

  handleFileInput(event: Event) {
    var tmpFile = (event.currentTarget as HTMLInputElement).files?.item(0);
    if (tmpFile != undefined) {
      this.fileToUpload = tmpFile;
      this.namefile = this.fileToUpload.name;
    }
  }

  openModal(id: string) {
    this.modalService.open(id);
  }

  closeModal(id: string) {
    this.modalService.close(id);
  }
}
