import { Component, Input, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { ModalService } from 'src/app/components/modal/modalService';
import { ITreeView } from 'src/app/date/ITreeView';
import { PrototypeInitFileService } from 'src/app/services/prototype_initfile.service';
import { Stack } from 'stack-typescript';

@Component({
    selector: 'app-prototype',
    templateUrl: './prototypeInitfile.page.component.html',
})
export class PrototypeInitfileComponent implements OnInit {

    treeView: ITreeView;
    treeViewChildStack: Stack<ITreeView[]> = new Stack();
    currentContextPath: Stack<string> = new Stack();

    name_initfile: string;
    version_initfile: string;

    fileControl: FormGroup | undefined;
    aiControl: FormGroup | undefined;
    loadAi: boolean = false;
    outputAi: string | undefined;
    fileCreateControl: FormGroup = new FormGroup({
        nameFile: new FormControl(''),
        typeFile: new FormControl('')
    })

    constructor(private prototypeInitFileService: PrototypeInitFileService,
        private activatedRoute: ActivatedRoute,
        private modalService: ModalService) {

    }

    ngOnInit(): void {
        console.log("Init")


        this.activatedRoute.queryParams.subscribe(params => {
            this.name_initfile = params['name'];
            this.version_initfile = params['version'];
            this.prototypeInitFileService.viewDir(this.name_initfile, this.version_initfile, '/')
                .subscribe((res: any) => {
                    this.treeView = res;
                    if (this.treeView.children != undefined) {
                        this.treeViewChildStack.push(this.treeView.children[0].children || []);
                    } else {
                        console.log(this.treeView.children);
                    }
                    console.log(res);
                });
        });
    }

    sendContextAndText() {
        if (this.fileControl == undefined || this.aiControl == undefined) {
            console.error('fileControll or aiControll is undefined')
            return;
        }
        let fileContent = this.fileControl.controls['content'].value;
        let aiContent = this.aiControl.controls['content'].value;
        this.loadAi = true;
        console.log(fileContent + ' ' + aiContent)
        this.prototypeInitFileService.aiService(
            fileContent,
            aiContent
        ).subscribe((res: any) => {
            this.outputAi = res.predictions;
            this.loadAi = false;
            // this.outputAi = this.outputAi?.replace(fileContent, "").replace(aiContent, "");
        });
    }

    saveFile() {
        if (this.fileControl == undefined) {
            console.error(this.fileControl + ' is undefined')
            return;
        }
        this.prototypeInitFileService.updateFile(this.name_initfile, this.version_initfile,
            this.currentContextPath.toArray().reverse().join('/'),
            this.fileControl.controls['nameFile'].value,
            this.fileControl.controls['content'].value, 'update').subscribe((res) => {
                console.log(res);
            })
    }

    deleteFile(namefile: string) {
        if (this.fileControl == undefined) {
            console.error(this.fileControl + ' is undefined')
            return;
        }
        this.prototypeInitFileService.updateFile(this.name_initfile, this.version_initfile,
            this.currentContextPath.toArray().reverse().join('/'),
            namefile,
            '', 'delete').subscribe((res) => {
                console.log(res);
                this.ngOnInit();

                if (this.fileControl != undefined) {
                    this.fileControl.controls['nameFile'].setValue('');
                    this.fileControl.controls['content'].setValue('');
                }

            })
    }

    createFile() {
        this.prototypeInitFileService.updateFile(this.name_initfile, this.version_initfile,
            this.currentContextPath.toArray().reverse().join('/'),
            this.fileCreateControl.controls['nameFile'].value,
            '', 'create', this.fileCreateControl.controls['typeFile'].value).subscribe((res) => {
                console.log(res);

                this.ngOnInit();
                this.closeModal('custom-modal-2');
            })
    }

    openDir(name: string) {
        this.fileControl = undefined;
        this.treeViewChildStack.head.forEach(
            (tview: ITreeView) => {
                if (tview.name == name) {
                    this.currentContextPath.push(name);
                    this.treeViewChildStack.push(tview.children || []);
                }
            }
        );
    }

    openFile(name: string) {
        this.prototypeInitFileService.openFile(name, this.currentContextPath.toArray().reverse().join('/'),
            this.name_initfile, this.version_initfile).subscribe((res) => {
                console.log(res);

                this.fileControl = new FormGroup({
                    nameFile: new FormControl(name),
                    content: new FormControl(res)
                });

                this.aiControl = new FormGroup({
                    content: new FormControl('')
                });
            })
    }

    loadZip() {
        this.prototypeInitFileService.loadFile(this.name_initfile, this.version_initfile)
    }

    backDir() {
        this.currentContextPath.pop();
        this.treeViewChildStack.pop();
    }


    openModal(id: string) {
        this.modalService.open(id);
    }

    closeModal(id: string) {
        this.modalService.close(id);
    }
}
