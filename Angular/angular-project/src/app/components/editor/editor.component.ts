import { AfterViewInit, Component, ElementRef, Input, OnChanges, OnInit, ViewChild } from '@angular/core'
import { FormGroup } from '@angular/forms';

declare var CodeMirror: any

@Component({
    selector: 'editor',
    template: `
    <textarea #editor style="height: 100%; width: 100%">
    </textarea>
`,
    styleUrls: [
        '../../../../node_modules/codemirror/lib/codemirror.css'
    ]
})

export class EditorComponent implements AfterViewInit, OnInit, OnChanges {
    @ViewChild('editor') editor: any;
    @Input() fileControl: FormGroup
    editorMirror: any;

    constructor() {
    }

    ngOnInit() {
    }

    ngAfterViewInit(): void {
        this.editorMirror = new CodeMirror.fromTextArea(this.editor.nativeElement, {
            lineNumbers: true,
            lineWrapping: true,
            styleActiveLine: true,
            autoRefresh: true,
            mode: 'text/x-yaml',
            theme: "monokai",
        }
        );

        this.editorMirror.on('change', (editor: any) => {
            console.log(this.editorMirror.getDoc().getValue());

            this.fileControl.controls['content'].setValue(this.editorMirror.getDoc().getValue());
        });

        this.editorMirror.setValue(this.fileControl.controls['content'].value)

        this.fileControl.controls['content'].valueChanges.subscribe((new_value: string) => {
            if (new_value != this.editorMirror.getDoc().getValue()) {
                this.editorMirror.setValue(new_value)
            }
        })  

        this.editorMirror.setSize('100%', '900px')
    }

    ngOnChanges() {
        this.editorMirror.setValue(this.fileControl.controls['content'].value)
        //save form
    }

}