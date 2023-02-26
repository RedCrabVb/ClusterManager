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
        console.log(this.fileControl);
    }

    ngAfterViewInit(): void {
        console.log(this.editor.nativeElement)
        this.editorMirror = new CodeMirror.fromTextArea(this.editor.nativeElement, {
            lineNumbers: true,
            lineWrapping: true,
            styleActiveLine: true,
            autoRefresh: true,
            mode: 'text',
            theme: "monokai",
        }
        );
        console.log(this.editorMirror)

        this.editorMirror.on('change', (editor: any) => {
            console.log(this.editorMirror.getDoc().getValue());

            this.fileControl.controls['content'].setValue(this.editorMirror.getDoc().getValue());
        });

        console.log(this.fileControl)

        this.editorMirror.setValue(this.fileControl.controls['content'].value)

        this.fileControl.controls['content'].valueChanges.subscribe((new_value: string) => {
            if (new_value != this.editorMirror.getDoc().getValue()) {
                this.editorMirror.setValue(new_value)
            }
        })  

        let edRef = this.editorMirror
        console.log(this.fileControl.controls['content'].value)
    }

    ngOnChanges() {
        this.editorMirror.setValue(this.fileControl.controls['content'].value)
    }

}