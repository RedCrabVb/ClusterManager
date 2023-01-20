import { Component, Input } from '@angular/core';
import { product as data } from '../../date/product';
import { ProductsService } from '../../services/Products.service'; 
import { InitFileService } from '../../services/initfile.service'; 
import { HostsService } from 'src/app/services/hosts.service';
import { ModalService } from 'src/app/components/modal/modalService';
import { IHost } from 'src/app/date/IHost';

@Component({
  selector: 'app-welcome',
  templateUrl: './hosts.page.html',
})
export class HostsComponent {
    hosts = [
        {
            "hostname": "192.176",
            "username": "root"
        }
    ]

    hostAdd: IHost = {
        hostname: '',
        username: '',
        password: ''
    }

    
    constructor(private hostsService: HostsService, private modalService: ModalService) {

    }

    addHost() {
        this.hostsService.addHosts(this.hostAdd).subscribe((res) => console.log(res))
        console.log('add host')
    }

    testConnection() {
        console.log('test connection')

        this.hostsService.testConnection(this.hostAdd).subscribe((res) => {console.log(res)})
    }

    updatePropHostname(event: any) {
        this.hostAdd.hostname = event.target.value;
        console.log(this.hostAdd)
    }


    updatePropUsername(event: any) {
        this.hostAdd.username = event.target.value;
        console.log(this.hostAdd)
    }

    updatePropPassword(event: any) {
        this.hostAdd.password = event.target.value;
        console.log(this.hostAdd)
    }


    openModal(id: string) {
        this.modalService.open(id);
    }

    closeModal(id: string) {
        this.modalService.close(id);
    }
}