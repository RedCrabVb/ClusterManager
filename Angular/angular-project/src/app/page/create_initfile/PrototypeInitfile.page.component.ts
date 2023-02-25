import { Component, Input, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { ITreeView } from 'src/app/date/ITreeView';
import { PrototypeInitFileService } from 'src/app/services/prototype_initfile.service';
import { Stack } from 'stack-typescript';
// import 'ace-builds/webpack-resolver';

@Component({
    selector: 'app-prototype',
    templateUrl: './PrototypeInitfile.page.component.html',
})
export class PrototypeInitfileComponent implements OnInit {

    treeView: ITreeView
    treeViewChildStack: Stack<ITreeView[]> = new Stack()
    currentContextPath: Stack<string> = new Stack()

    name_initfile: string
    version_initfile: string

    fileControl: FormGroup | undefined



    title = 'angular-code-editor';
    jsonInputData = 'sdf';
    yamlInputData = '';
    appModuleTsData = '';
    scssData = '';

    constructor(private prototypeInitFileService: PrototypeInitFileService, private activatedRoute: ActivatedRoute) {

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
                    contnet: new FormControl(res)
                })
            })
    }

    backDir() {
        this.currentContextPath.pop();
        this.treeViewChildStack.pop();
    }

}
